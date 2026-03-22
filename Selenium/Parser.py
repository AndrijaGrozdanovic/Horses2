from bs4 import BeautifulSoup
from Selenium.browserSession import BrowserSession


class Parser(object):
    def __init__(self, url, res: str = 'Results'):
        obj = BrowserSession(url)
        if res == 'Results':
            obj.extractRacePageSource()
        elif res == 'Date':
            obj.extractDatePageSource()
        elif res == 'RaceCard':
            obj.extractRaceCardPageSource()
        elif res == 'RaceCardDate':
            obj.RCDate()
        self.mainPage = obj.obj.mainPage
        self.BS = BeautifulSoup(obj.pageSource, "lxml")
        self.url = url
