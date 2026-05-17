from Selenium.Parser import Parser
import re


def build_non_runner_query(horse_names):
    string = str(horse_names).replace('[', '(').replace(']', ')')

    if horse_names:
        return f'''
        DELETE FROM Race_Card_turf_handicap
        WHERE horseNameRaw IN {string}
        '''

    return 'SELECT * FROM Race_Card_turf_handicap WHERE 1=2'


def BHANonRunners():
    BHAUpdate = Parser('https://www.britishhorseracing.com/racing-updates/', 'BHA')
    horses = [h.get_text(strip=True).replace("'", "") for h in BHAUpdate.BS.select('h3[ng-bind="item.data.horseName"]')]
    horse_names = [re.sub(r'\s*\([A-Z]+\)$', '', h) for h in horses]
    return build_non_runner_query(horse_names)


def RPNonRunners(raceDate):
    RC = Parser(f'https://www.racingpost.com/racecards/{raceDate}', 'RaceCardDate')
    meetings = [f'https://www.racingpost.com{a.get('href')}' for a in RC.BS.find_all('a', class_='RC-meetingList__showAll ui-link ui-link_table')]
    horse_names = []
    for meeting in meetings:
        trackID = int(meeting.split('/')[4])
        if (trackID <= 203 or trackID == 596 or trackID == 1212) and trackID != 186:
            MeetBS = Parser(meeting, 'RPNR')
            non_runners = MeetBS.BS.select('span.RC-runnerNumber__no_nonRunner[data-test-selector="RC-cardPage-runnerNumber-no"]')
            NRs = [el.get("data-horsename").replace("'", "") for el in non_runners]
            horse_names.extend(NRs)
        return build_non_runner_query(horse_names)
