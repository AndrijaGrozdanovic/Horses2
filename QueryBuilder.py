from collections import defaultdict
from JsonReader.JsonReader import JsonReader


jsonFile = JsonReader("OverallFilter.json")
filters = jsonFile.data

conditions = [(col, cond) for col, conds in filters.items() for cond in conds]
condition_to_bit = {cond: i for i, cond in enumerate(conditions)}


def parse_condition(cond):
    if cond.startswith((">=", "<=")):
        return cond[:2], cond[2:]
    elif cond.startswith((">", "<", "=")):
        return cond[0], cond[1:]
    else:
        raise ValueError(cond)


def build_mask_sql():
    parts = defaultdict(list)

    for (col, cond), idx in condition_to_bit.items():
        op, val = parse_condition(cond)

        mask_id = idx // 63 + 1
        bit_pos = idx % 63

        sql = f"CASE WHEN {col} {op} {val} THEN POWER(CAST(2 AS BIGINT), {bit_pos}) ELSE 0 END"
        parts[mask_id].append(sql)

    return parts


def create_Turf_2026_masked(masks):

    query_parts = []

    query_parts.append("DROP TABLE IF EXISTS Turf_2026_masked;\n")
    query_parts.append("SELECT *,")

    for i in sorted(masks.keys()):
        if i > 2:
            break

        mask_expr = "(\n  " + "\n+ ".join(masks[i]) + f"\n) AS mask{i},"
        query_parts.append(mask_expr)

    query_parts.append("INTO Turf_2026_masked")
    query_parts.append("FROM Turf_2026;")

    query = "\n".join(query_parts)
    return query


mask_parts = build_mask_sql()


query_for_injection = create_Turf_2026_masked(mask_parts)

print(query_for_injection)
