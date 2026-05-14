from Selenium.Parser import Parser
import re


def BHANonRunners():
    BHAUpdate = Parser('https://www.britishhorseracing.com/racing-updates/', 'BHA')
    horses = [h.get_text(strip=True).replace("'", "") for h in BHAUpdate.BS.select('h3[ng-bind="item.data.horseName"]')]
    horse_names = [re.sub(r'\s*\([A-Z]+\)$', '', h) for h in horses]
    string = str(horse_names).replace('[', '(').replace(']', ')')
    if len(horse_names) > 0:
        query = f'Delete from Race_Card_turf_handicap where horseNameRaw in {string}'
    else:
        query = 'select * from Race_Card_turf_handicap where 1=2'
    return query


def RPNonRunners():
    RC = Parser('https://www.racingpost.com/racecards/2026-05-15', 'RaceCardDate')
    meetings = [f'https://www.racingpost.com{a.get('href')}' for a in RC.BS.find_all('a', class_='RC-meetingList__showAll ui-link ui-link_table')]
    horse_names = []
    for meeting in meetings:
        MeetBS = Parser(meeting, 'RPNR')
        non_runners = MeetBS.BS.select(
            'span.RC-runnerNumber__no_nonRunner[data-test-selector="RC-cardPage-runnerNumber-no"]'
        )

        NRs = [
            el.get("data-horsename").replace("'", "")
            for el in non_runners
        ]

        horse_names.extend(NRs)
    string = str(horse_names).replace('[', '(').replace(']', ')')
    if len(horse_names) > 0:
        query = f'Delete from Race_Card_turf_handicap where horseNameRaw in {string}'
    else:
        query = 'select * from Race_Card_turf_handicap where 1=2'
    return query


if __name__ == '__main__':

    print(BHANonRunners())
    print(RPNonRunners())


