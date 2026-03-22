import pandas as pd

from Selenium.Parser import Parser
from Selenium.ResultsPageRunners import ResultsPageRuners
from Selenium.ResultsPageRaceHeader import ResultsPage
from Selenium.RaceCardHeader import RaceCardHeader
from Selenium.RaceCardRunner import RaceCardRunners

import os
import glob
import logging
import shutil


def frameResults(url):
    final_df = pd.DataFrame()
    browser = Parser(url)

    RaceHeader = ResultsPage(browser.BS, browser.url)
    RaceHeader.setAll()

    filename = f'{RaceHeader.raceDate}_{RaceHeader.raceTime.replace(":", "")}_{RaceHeader.track}'

    obj = ResultsPageRuners(browser.BS)
    obj.setResults()

    df_runners = pd.DataFrame(obj.data)
    df_race = pd.DataFrame([RaceHeader.data])
    df_race_expanded = pd.concat([df_race] * len(df_runners), ignore_index=True)
    final_df = pd.concat([df_race_expanded, df_runners], axis=1)

    final_df['oddDif'] = final_df['SP'] - final_df['SP'].min()
    final_df = final_df.reset_index(drop=True)
    final_df["runnerID"] = (final_df["raceID"].astype(str) + final_df.index.astype(str).str.zfill(2))
    final_df['winningDistance'] = pd.to_numeric(final_df['winningDistance'], errors='coerce')
    final_df['winningDistance'] = final_df['possition'].apply(
        lambda x: float(final_df['winningDistance'].min()) if (x == 1) else None)
    final_df = final_df.infer_objects(copy=False)

    final_df.to_csv(rf'd:\SeleniumDrop\{filename}.csv', index=False)


def raceCardFrame(url):
    final_df = pd.DataFrame()
    Page = Parser(url, 'RaceCard')
    Header = RaceCardHeader(Page.BS, Page.url)
    Header.rcSetAll()
    Runners = RaceCardRunners(Page.BS)
    for row in Runners.rowList:
        Runners.setParameters(row)
    df_runners = pd.DataFrame(Runners.data)
    df_race = pd.DataFrame([Header.data])
    df_race_expanded = pd.concat([df_race] * len(df_runners), ignore_index=True)
    final_df = pd.concat([df_race_expanded, df_runners], axis=1)
    final_df.to_csv(rf'd:\test.csv', index=False)
def import_csv_folder(folder_path, con, table_name):

    failed_folder = os.path.join(folder_path, "failed")
    os.makedirs(failed_folder, exist_ok=True)

    logging.basicConfig(
        filename="d:/csv_import_errors.log",
        level=logging.ERROR,
        format="%(asctime)s - %(message)s"
    )

    files = glob.glob(os.path.join(folder_path, "*.csv"))

    # print(f"{len(files)} files found")

    for file in files:

        # print(f"Importing {file}")

        try:

            df = pd.read_csv(file)
            df = df.replace('', None)

            df.to_sql(
                table_name,
                con,
                if_exists="append",
                index=False,
                method="multi"
            )

            # print(f"Imported {len(df)} rows")

        except Exception as e:

            logging.error(f"FAILED FILE: {file}")
            logging.error(str(e))

            dest = os.path.join(failed_folder, os.path.basename(file))
            shutil.move(file, dest)

            print(f"Moved to failed: {dest}")

    print("\nImport finished")
