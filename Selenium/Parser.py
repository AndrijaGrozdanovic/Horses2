from bs4 import BeautifulSoup
from Selenium.browserSession import BrowserSession


class Parser(object):
    def __init__(self, url, res: bool = True):
        obj = BrowserSession(url)
        if res:
            obj.extractRacePageSource()
        else:
            obj.extractDatePageSource()
        self.BS = BeautifulSoup(obj.pageSource, "lxml")
        self.url = url
