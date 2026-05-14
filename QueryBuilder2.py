from collections import defaultdict
from itertools import combinations, product
from database.DBConnection import DbConnection
from JsonReader.JsonReader import JsonReader

jsonFile = JsonReader("HGfilter.json")
output_file = f"d:/{jsonFile.file_name.replace('.json', '.sql')}"
filters = jsonFile.data
# output_file = "d:/combinations_mask_inserts.sql"

conditions = [(col, cond) for col, conds in filters.items() for cond in conds]
condition_to_bit = {cond: i for i, cond in enumerate(conditions)}

obj = DbConnection('mssql')
obj.createConnection("AUTOCOMMIT")
con = obj.connection

# obj.executeQuery(f"EXEC dbo.Drop_Tables_ByPrefix @Prefix = 'combinations_mask',@SchemaName = 'dbo';")


def build_combo_masks(max_k=3):
    columns = list(filters.keys())

    for k in range(2, max_k + 1):
        for cols in combinations(columns, k):

            cond_lists = [filters[col] for col in cols]

            for cond_choice in product(*cond_lists):
                masks = {}
                sql_parts = []

                for col, cond in zip(cols, cond_choice):
                    bit = condition_to_bit[(col, cond)]
                    mask_id = bit // 63
                    bit_pos = bit % 63

                    masks.setdefault(mask_id, 0)
                    masks[mask_id] |= (1 << bit_pos)

                    sql_parts.append(build_sql_condition(col, cond))

                where_sql = " AND ".join(sql_parts)

                yield (
                    masks.get(0, 0),
                    masks.get(1, 0),
                    where_sql
                )


def parse_condition(cond):
    cond = cond.strip()

    if cond.startswith((">=", "<=")):
        return cond[:2], cond[2:].strip()
    elif cond.startswith((">", "<", "=")):
        return cond[0], cond[1:].strip()
    else:
        return None, cond  # no operator


def build_sql_condition(column, cond):
    op, val = parse_condition(cond)

    # detect numeric
    try:
        float(val)
        is_numeric = True
    except ValueError:
        is_numeric = False

    # 🔥 FORCE equality if no operator
    if op is None:
        if is_numeric:
            return f"{column} = {val}"
        else:
            return f"{column} = '{val}'"

    # normal operator handling
    if is_numeric:
        return f"{column} {op} {val}"
    else:
        return f"{column} {op} '{val}'"


def build_mask_sql():
    parts = defaultdict(list)

    for (col, cond), idx in condition_to_bit.items():
        mask_id = idx // 63 + 1
        bit_pos = idx % 63

        condition_sql = build_sql_condition(col, cond)

        sql = (
            f"CASE WHEN {condition_sql} "
            f"THEN POWER(CAST(2 AS BIGINT), {bit_pos}) ELSE 0 END"
        )

        parts[mask_id].append(sql)

    return parts


def create_Turf_2026_masked(masks):
    query_parts = []
    query_parts.append("DROP TABLE IF EXISTS Turf_2026_masked;\n")
    query_parts.append("SELECT *,")

    mask_columns = []

    for i in sorted(masks.keys()):
        if i > 2:
            break

        mask_expr = "(\n  " + "\n+ ".join(masks[i]) + f"\n) AS mask{i}"
        mask_columns.append(mask_expr)

    # join with commas ONLY between items
    query_parts.append(",\n".join(mask_columns))

    query_parts.append("\nINTO Turf_2026_masked")
    query_parts.append("FROM Turf_2026;")

    query = "\n".join(query_parts)
    return query


mask_parts = build_mask_sql()

query_for_injection = create_Turf_2026_masked(mask_parts)

obj.executeQuery(query_for_injection)

print('Turf_2026_masked Created')

# Creating .sql file which will insert data into combinations_mask_N tables


obj.executeQuery(f'exec create_combinations_table combinations_mask')

with open(output_file, "w", encoding="utf-8") as f:
    f.write("SET NOCOUNT ON;\n\n")

    for i, row in enumerate(build_combo_masks(max_k=5)):
        m1, m2, sql = row
        # table_id = i % number_of_tables + 1
        safe_sql = (sql + " AND Favourite IS NOT NULL").replace("'", "''")

        sql1 = f"""
        INSERT INTO combinations_mask
        (mask1, mask2, condition_sql)
        VALUES ({m1}, {m2}, '{safe_sql}');
        """
        obj.executeQuery(sql1)
        f.write(sql1)
        if i % 10000 == 0:
            print(f"Written {i} rows...")

print(f"Done → {output_file}")
