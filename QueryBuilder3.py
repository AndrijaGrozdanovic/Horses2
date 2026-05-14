import polars as pl
from database.DBConnection import DbConnection
import numpy as np


def run_k_results(table_name):
    result_table = "k_results_HG"
    chunk_size = 100_000

    obj = DbConnection('mssql')
    obj.createConnection("AUTOCOMMIT")
    con = obj.connection

    print(f"\n🚀 Running for: {table_name}")

    # --- Load data with YEAR + MONTH ---
    df = pl.read_database("""
        SELECT 
            mask1, 
            mask2, 
            YEAR(raceDate) AS yr,
            MONTH(raceDate) AS mn,
            profit_SP
        FROM Turf_2026_masked 
        WHERE Favourite IS NOT NULL
    """, con)

    comb = pl.read_database(
        f"SELECT id, mask1, mask2 FROM {table_name}",
        con
    )

    # --- Convert to NumPy ---
    mask1_arr = comb["mask1"].to_numpy()
    mask2_arr = comb["mask2"].to_numpy()
    ids = comb["id"].to_numpy()

    df_np_mask1 = df["mask1"].to_numpy()
    df_np_mask2 = df["mask2"].to_numpy()
    df_np_profit = df["profit_SP"].to_numpy()
    df_np_year = df["yr"].to_numpy()
    df_np_month = df["mn"].to_numpy()

    results = []

    # --- Main loop ---
    for i in range(len(mask1_arr)):

        if i % 1000 == 0:
            print(f"Processed {i}/{len(mask1_arr)}")

        m1 = mask1_arr[i]
        m2 = mask2_arr[i]

        mask = ((df_np_mask1 & m1) == m1) & ((df_np_mask2 & m2) == m2)

        if not mask.any():
            continue

        profits = df_np_profit[mask]

        total_profit_all = profits.sum()
        total_samples_all = len(profits)
        wins_all = (profits > 0).sum()  # ✅ TRUE winrate per bet
        years = df_np_year[mask]
        months = df_np_month[mask]
        equity = profits.cumsum()
        max_dd = (equity - np.maximum.accumulate(equity)).min()

        # combine year+month into one key (fast grouping trick)
        ym = years * 100 + months  # e.g. 202405

        unique_ym = np.unique(ym)

        for val in unique_ym:
            submask = (ym == val)
            vals = profits[submask]

            results.append({
                "id": int(ids[i]),
                "year": int(val // 100),
                "month": int(val % 100),

                "sample_size": int(len(vals)),
                "total_profit": float(vals.sum()),
                "avg_profit": float(vals.mean()),
                "max_profit": float(vals.max()),

                # ✅ partition-by-id values
                "total_profit_all": float(total_profit_all),
                "total_samples_all": int(total_samples_all),
                "winrate_all": float(wins_all / total_samples_all),
                "max_drawdown_all": float(max_dd)
            })

        # --- chunk flush ---
        if len(results) >= chunk_size:
            pl.DataFrame(results).write_database(
                table_name=result_table,
                connection=con,
                if_table_exists="append"
            )
            results = []

    # --- final flush ---
    if results:
        pl.DataFrame(results).write_database(
            table_name=result_table,
            connection=con,
            if_table_exists="append"
        )

    print(f"✅ Done: {table_name}")
    con.close()


if __name__ == "__main__":
    run_k_results('combinations_mask')
