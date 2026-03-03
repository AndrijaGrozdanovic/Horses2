import pandas as pd

from Selenium.Parser import Parser
from Selenium.ResultsPageRunners import ResultsPageRuners
from Selenium.ResultsPageRaceHeader import ResultsPage


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


# if __name__ == '__main__':
#
#     resUrl = ['https://www.racingpost.com/results/93/windsor/2025-05-05/892635',
#               'https://www.racingpost.com/results/1079/kempton-aw/2025-05-05/893022']
#     for link in resUrl:
#         frameResults(link)
