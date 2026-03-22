import re
from Parser import Parser
from multiprocessing import Pool
from ResultsPageRaceHeader import ResultsPage
from ResultsPageRunners import ResultsPageRuners
from DataFrame import DataFrame
from DataFrame.ResultsDataframe import frameResults, raceCardFrame
import time


def pickResultsPerDate(date):
    link = f'https://www.racingpost.com/results/{date}/time-order'
    selDRV = Parser(link, 'Date')
    soup = selDRV.BS
    links = []

    # Adjust this selector to the wrapper element that contains both blocks

    race_blocks = soup.select("div.rp-timeView__raceInfo.ng-isolate-scope")

    if len(race_blocks) == 0:
        return

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
            links.append('https://www.racingpost.com' + result_link)
        # just to see if GUI works
    return links


def pickRaceCards(url):
    selDRV = Parser(url, 'RaceCardDate')

    links = []
    for ahtml in selDRV.BS.find_all('a', class_='RC-meetingItem__link'):
        trackID = int(re.split(r'/', ahtml.get('href'))[2])
        if not ('Hurdle' in ahtml.text or 'Chase' in ahtml.text) and 'Handicap' in ahtml.text and (
                trackID <= 203 or trackID == 596 or trackID == 1212) and trackID != 186:
            links.append(selDRV.mainPage + ahtml.get('href'))
        else:
            pass
    print(links)


def getRaceLinks(dateList):
    races = []
    for date in dateList:
        try:
            for race in pickResultsPerDate(date):
                races.append(race)
        except TypeError:
            continue
    return races


if __name__ == '__main__':
    pickRaceCards('https://www.racingpost.com/racecards/')
    # [frameResults(link) for link in getRaceLinks(DataFrame.DateList('2015-11-16', '2015-12-31'))]
    # DateURLs = DataFrame.DateList('2016-03-15', '2016-03-31')
    #
    # # link = 'https://www.racingpost.com/results/5/bath/2025-05-23/893863'
    # # frameResults(link)
    #
    # DateURLs = ['2020-09-12']
    # Races = getRaceLinks(DateURLs)
    #
    # for race in Races:
    #     frameResults(race)

    # p = Pool(10)
    # p.map(frameResults, Races)
    # p.terminate()
