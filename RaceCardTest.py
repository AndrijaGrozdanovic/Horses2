


from DataFrame.ResultsDataframe import raceCardFrame

from Selenium.Parser import Parser
if __name__ == '__main__':
    url = 'https://www.racingpost.com/racecards/2026-04-04/'
    obj = Parser(url, 'RaceCardDate')
