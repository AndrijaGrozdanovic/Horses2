from collections import defaultdict
from JsonReader.JsonReader import JsonReader




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


mask_parts = build_mask_sql()

print("SELECT *,")
for i in sorted(mask_parts.keys()):
    if i > 2:
        break   # ✅ only mask1 + mask2
    print("(\n  " + "\n+ ".join(mask_parts[i]) + f"\n) AS mask{i},")

print("INTO Turf_2026_masked")
print("FROM Turf_2026;")
