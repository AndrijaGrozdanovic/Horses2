import polars as pl
from database.DBConnection import DbConnection

obj = DbConnection('mssql')
obj.createConnection("AUTOCOMMIT")
con = obj.connection

df = pl.read_database("""
SELECT
    runnerID,
    raceDate,
    horseName,
    HG
FROM Turf_2026
""", connection=con)


df = (df.with_columns(pl.when(pl.col("HG").is_null()).then(None).otherwise(pl.col("HG").str.replace(r"\d+$", "")).alias("hg_clean")).sort(["horseName", "raceDate"]))


def mark_returns(g):
    seen = set()
    last_hg = None
    out = []

    for hg in g["hg_clean"]:
        if hg is None:
            out.append(0)
            last_hg = None
            continue

        if hg in seen and hg != last_hg:
            out.append(1)
        else:
            out.append(0)

        seen.add(hg)
        last_hg = hg

    return g.with_columns(pl.Series("HG_return", out))


df = (df.group_by("horseName", maintain_order=True).map_groups(mark_returns))

df.write_database(table_name="HG_return", connection=con, if_table_exists="replace")
