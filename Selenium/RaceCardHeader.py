import re


class RaceCardHeader(object):
    data = {}

    def __init__(self, BSimport, url):
        self.url = url
        self.raceDetails = BSimport.find('div', class_='RC-cardHeader__courseDetails RC-cardHeader__courseDetails--desktop')
        self.raceInfo = BSimport.find('div', class_='RC-courseHeader')
        self.raceKeyInfo = BSimport.find('div', class_='RC-headerBox')
        self.track = ""
        self.raceTime = ""
        self.raceName = ""
        self.raceType = "Turf"
        self.raceType1 = "Flat"
        self.raceDate = ""
        self.month = ""
        self.handicap = ""
        self.distance = ""
        self.yards = ""
        self.ageLimit = ""
        self.ORLimitNumerical = ""
        self.raceClass = ""
        self.raceClassNumeric = None
        self.numberOfFences = ""
        self.prizeMoney = ""

    def fetchRaceInfo(self):
        self.raceTime = self.raceInfo.find('span', class_='RC-courseHeader__time').text.strip()
        self.track = self.raceInfo.find('h1').text.strip()

    @classmethod
    def handleDataSelector(cls, string, elementList):
        parameter = ''
        for element in elementList:
            try:
                if element.get('data-test-selector') == string:
                    parameter = element.text.strip()
            except AttributeError:
                pass
        return parameter

    @staticmethod
    def calculateYards(rawInput):
        try:
            m = re.findall(r'(\d+)(?=\s*m)', rawInput)[0]
        except IndexError:
            m = 0
        try:
            f = re.findall(r'(\d+)(?=\s*f)', rawInput)[0]
        except IndexError:
            f = 0
        try:
            yds = re.findall(r'(\d+)(?=\s*yds)', rawInput)[0]
        except IndexError:
            yds = 0
        yards = 1760 * int(m) + 220 * int(f) + int(yds)
        return yards

    def fetchRaceDetails(self):
        self.distance = RaceCardHeader.handleDataSelector('RC-header__raceDistanceRound', self.raceDetails)
        self.yards = self.calculateYards(self.distance)
        if self.yards == 0:
            self.distance = RaceCardHeader.handleDataSelector('RC-header__raceDistance', self.raceDetails)
            self.yards = self.calculateYards(self.distance)

        self.raceName = RaceCardHeader.handleDataSelector('RC-header__raceInstanceTitle', self.raceDetails)

        if 'Handicap' in self.raceName:
            self.handicap = 'Hcap'
        else:
            self.handicap = 'NonHcap'

        if 'Hurdle' in self.raceName:
            self.raceType = 'Hurdle'
            self.raceType1 = 'Hurdle'

        if 'Chase' in self.raceName:
            self.raceType = 'Chase'
            self.raceType1 = 'Chase'

        if 'Steeplechase' in self.raceName:
            self.raceType = 'Chase'
            self.raceType1 = 'Chase'

        if ' Hdl ' in self.raceName:
            self.raceType = 'Hurdle'
            self.raceType1 = 'Hurdle'

        Limit_info = RaceCardHeader.handleDataSelector('RC-header__rpAges', self.raceDetails)
        self.ageLimit = Limit_info.split(' ')[0].replace('(','').replace(')','')
        try:
            self.ORLimitNumerical = Limit_info.split(' ')[1].split('-')[1].replace(')','')
        except IndexError:
            pass
        self.raceClass = RaceCardHeader.handleDataSelector('RC-header__raceClass', self.raceDetails).replace('(','').replace(')','')
        try:
            self.raceClassNumeric = int(re.findall(r'\d', self.raceClass)[0])
        except IndexError:
            pass

    def fetchRaceKeyInfo(self):
        try:
            self.numberOfFences = int(RaceCardHeader.handleDataSelector('RC-headerBox__stalls', self.raceKeyInfo).split('\n')[1].strip())
        except (ValueError, IndexError):
            pass

        try:
            self.prizeMoney = int(RaceCardHeader.handleDataSelector('RC-headerBox__winner', self.raceKeyInfo).split('\n')[1].strip().replace('€','').replace('£','').replace(',',''))
        except ValueError:
            pass

    def getDateAndMonth(self):
        self.raceDate = self.url.split('/')[6]
        self.month = str(self.raceDate).split('-')[1]

    def rcSetAll(self):
        self.fetchRaceInfo()
        self.fetchRaceDetails()
        self.fetchRaceKeyInfo()
        self.getDateAndMonth()
        self.data = self.__dict__.copy()
        self.data.pop('driver', None)
        self.data.pop('url', None)
        self.data.pop('raceDetails', None)
        self.data.pop('raceInfo', None)
        self.data.pop('raceKeyInfo', None)

        print(self.data)


