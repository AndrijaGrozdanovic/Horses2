import re
import logging


class ResultsPage(object):
    data = {}

    def __init__(self, BSimport, url):
        self.url = url
        self.html = BSimport.find('div', class_='rp-raceTimeCourseName')
        self.htmlRaceInfo = BSimport.find('div', class_='rp-raceInfo')
        self.raceName = ''
        self.raceDate = ''
        self.noOfFences = ''
        self.raceType = 'Turf'
        self.raceType1 = 'Flat'
        self.raceTime = ''
        self.raceClass = ''
        self.raceClassNumeric = ''
        self.track = ''
        self.distance = ''
        self.yards = ''
        self.ageLimit = ''
        self.going = ''
        self.wtime = ''
        self.ORLimit = ''
        self.ORLimitNumeric = ''
        self.handicap = ''
        self.prize = ''
        self.raceID = ''
        self.courseID = ''

    def getRaceName(self):
        try:
            self.raceName = self.html.find('h2', class_='rp-raceTimeCourseName__title').text
        except AttributeError:
            logging.error(f'Page not loaded properly')
        if 'Handicap' in self.raceName:
            self.handicap = 'Hcap'
        else:
            self.handicap = 'NonHcap'

        if 'Chase' in self.raceName:
            self.raceType = 'Chase'
            self.raceType1 = 'Chase'

        if 'Steeplechase' in self.raceName:
            self.raceType = 'Chase'
            self.raceType1 = 'Chase'

        if ' Hdl ' in self.raceName:
            self.raceType = 'Hurdle'
            self.raceType1 = 'Hurdle'

        if 'Hurdle' in self.raceName:
            self.raceType = 'Hurdle'
            self.raceType1 = 'Hurdle'

    def getTrack(self):
        try:
            self.track = self.html.select_one(
                'a.js-popupLink.ui-link.ui-link_table.ui-link_marked.rp-raceTimeCourseName__name').text.strip()
            if '(AW)' in self.track:
                self.raceType = 'AW'
            else:
                pass
        except AttributeError:
            logging.error(f'Page not loaded properly')

    def getRaceClass(self):
        try:
            self.raceClass = self.html.find('span', class_='rp-raceTimeCourseName_class').text.replace('(', '').replace(
                ')', '').strip()
            self.raceClassNumeric = int(re.findall(r'\d', self.raceClass)[0])
        except AttributeError:

            pass

    def getDistance(self):
        try:
            self.distance = self.html.find('span', class_='rp-raceTimeCourseName_distanceFull').text.replace('(',
                                                                                                             '').replace(
                ')', '').strip()
        except AttributeError:
            self.distance = self.html.find('span', class_='rp-raceTimeCourseName_distance').text.replace('(',
                                                                                                         '').replace(
                ')', '').strip()

        # Converting into Yards
        try:
            m = re.findall(r'(\d+)(?=\s*m)', self.distance)[0]
        except IndexError:
            m = 0
        try:
            f = re.findall(r'(\d+)(?=\s*f)', self.distance)[0]
        except IndexError:
            f = 0
        try:
            yds = re.findall(r'(\d+)(?=\s*yds)', self.distance)[0]
        except IndexError:
            yds = 0
        self.yards = 1760 * int(m) + 220 * int(f) + int(yds)

    def getPrizeMoney(self):
        try:
            self.prize = self.html.find('span', class_='rp-raceTimeCourseName__info_container').text.split('1st')[1].split('2nd')[0].strip().replace('£', '').replace('€', '').replace(',', '')
        except:
            pass
        try:
            float(self.prize)
        except ValueError:
            Prize_Money_temp = self.prize.split(' ')[0]
            self.prize = Prize_Money_temp

    def getORAndAgeLimitations(self):
        try:
            Race_info_limit = self.html.find('span', class_='rp-raceTimeCourseName_ratingBandAndAgesAllowed').text.replace('(', '').replace(')', '').strip()
        except AttributeError:
            Race_info_limit = ''
        try:
            Age_Limit_raw = re.split(',', Race_info_limit)[1].strip()
            try:
                OR_Limit_raw = re.split(',', Race_info_limit)[0].strip()
                OR_Limit_raw_numerical = re.split(',', Race_info_limit)[0].strip().split('-')[1]
            except (IndexError, TypeError):
                OR_Limit_raw = ''
                OR_Limit_raw_numerical = ''
        except IndexError:
            Age_Limit_raw = Race_info_limit.strip()
            OR_Limit_raw = ''
            OR_Limit_raw_numerical = ''

        self.ageLimit = Age_Limit_raw
        self.ORLimit = OR_Limit_raw
        self.ORLimitNumeric = OR_Limit_raw_numerical

    def getNumberOfFences(self):
        try:
            self.noOfFences = re.findall(r'\d+', self.html.find('span', class_='rp-raceTimeCourseName_hurdles').text)[0]
        except AttributeError:
            pass

    def getGoing(self):
        try:
            self.going = self.html.find('span', class_='rp-raceTimeCourseName_condition').text.replace('(', '').replace(
                ')', '').strip()
        except AttributeError:
            pass

    def getRaceTimeAndDate(self):
        try:
            dateTime = self.html.find('div', class_='rr-raceReplay').get('data-directive-race-replay-datetime')
            self.raceDate = dateTime.split('T')[0]
            self.raceTime = dateTime.split('T')[1][0:5]
        except AttributeError:
            pass

    def getRaceIDCourseID(self):
        self.raceID = self.url.split('/')[7]
        self.courseID = self.url.split('/')[4]

    def getWinningTimeSlowBy(self):
        try:
            raceInfo = re.findall(r'\(([^()]+)\)', self.htmlRaceInfo.select_one('ul > li:nth-child(1) > span:nth-child(3)').text)[0]
            number = re.findall(r'-?\d*\.\d+|\d+', raceInfo)[0]

            if 'slow' in raceInfo:
                self.wtime = -1 * float(number)
            else:
                self.wtime = float(number)

        except (AttributeError, IndexError):
            pass

    def setAll(self):
        self.getRaceName()
        self.getTrack()
        self.getRaceClass()
        self.getDistance()
        self.getPrizeMoney()
        self.getORAndAgeLimitations()
        self.getGoing()
        self.getRaceTimeAndDate()
        self.getRaceIDCourseID()
        self.getNumberOfFences()
        self.getWinningTimeSlowBy()

        self.data = self.__dict__.copy()
        self.data.pop('driver', None)
        self.data.pop('url', None)
        self.data.pop('html', None)
        self.data.pop('htmlRaceInfo', None)
