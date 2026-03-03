import re
from Parser import Parser
from multiprocessing import Pool
from ResultsPageRaceHeader import ResultsPage
from ResultsPageRunners import ResultsPageRuners
from DataFrame import DataFrame
from DataFrame.ResultsDataframe import frameResults
import time



def pickResultsPerDate(date):
    link = f'https://www.racingpost.com/results/{date}/time-order'
    selDRV = Parser(link, False)
    soup = selDRV.BS
    links = []

    # Adjust this selector to the wrapper element that contains both blocks
    race_blocks = soup.select("div.rp-timeView__raceInfo.ng-isolate-scope")

    for race in race_blocks:

        # Exclude Arabian races immediately
        is_arabian = race.select_one("span.rp-timeView__raceName__code_arabian")
        if is_arabian:
            continue

        # Normal country code
        code_span = race.select_one("span.rp-timeView__raceName__code")
        code = code_span.get_text(strip=True) if code_span else None

        link_tag = race.select_one("h4.rp-timeView__raceTitle a")
        result_link = link_tag["href"] if link_tag else None

        if result_link and code in (None, "(IRE)"):
            links.append('https://www.racingpost.com'+result_link)

    return links


def getRaceLinks(dateList):
    races = []
    for date in dateList:
        for race in pickResultsPerDate(date):
            races.append(race)
    return races


if __name__ == '__main__':
    # [frameResults(link) for link in getRaceLinks(DataFrame.DateList('2025-06-01', '2025-06-30'))]
    # [frameResults(link) for link in getRaceLinks(DataFrame.DateList('2025-07-01', '2025-10-31'))]
    DateURLs = DataFrame.DateList('2025-01-01', '2025-01-31')

    # link = 'https://www.racingpost.com/results/5/bath/2025-05-23/893863'
    # frameResults(link)

    Races = getRaceLinks(DateURLs)
    p = Pool(2)
    p.map(frameResults, Races)
    p.terminate()

