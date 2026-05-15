import re
from Selenium.Table import Table


class ResultsPageRuners(Table):
    def __init__(self, BSimport):
        Table.__init__(self, BSimport)
        self.noOfRunners = ''
        self.possition = ''
        self.prb2 = ''
        self.draw = ''
        self.dtwRaw = 0
        self.dtw = ''
        self.winningDistance = ''
        self.horseName = ''
        self.horseNameTrimmed = ''
        self.horseID = ''
        self.owner = ''
        self.ownerID = ''
        self.SP = ''
        self.favourite = ''
        self.jockey = ''
        self.jockeyID = ''
        self.jockeyClaim = ''
        self.trainer = ''
        self.trainerID = ''
        self.age = ''
        self.weight = ''
        self.OR = ''
        self.outOfHandicap = ''
        self.extraWeight = ''
        self.HG = ''
        self.WS = ''
        self.hColour = ''
        self.hType = ''
        self.hCategory = ''
        self.comment = ''
        self.sire = ''
        self.dam = ''
        self.damsSire = ''
        self.runnerID = ''
        self.data = []

    def setResults(self):

        self.getRows()
        for index, row in enumerate(self.mainRows):

            try:
                self.possition = int(row.find('span', class_='rp-horseTable__pos__number').text.strip().split('\xa0')[0])

            except ValueError:
                self.possition = 0
            # number of runners parameter, also used for PRB2
            self.noOfRunners = len(self.mainRows)
            try:
                if self.possition != 0:
                    self.prb2 = round(100 * ((self.noOfRunners - self.possition) / (self.noOfRunners - 1)) ** 2, 2)
                else:
                    self.prb2 = 0
            except ZeroDivisionError:
                self.prb2 = 0
            try:
                self.draw = row.find('sup', class_='rp-horseTable__pos__draw').text.strip().replace('(', '').replace(')', '').strip()
            except IndexError:
                pass

            # DTW parameter

            try:
                self.dtwRaw = row.select_one('span.rp-horseTable__pos__length > span:nth-child(2)').text.strip().replace('[', '').replace(']', '').strip()

            except AttributeError:
                try:
                    self.dtwRaw = row.select_one('span.rp-horseTable__pos__length > span:nth-child(1)').text.strip().replace('[', '').replace(']', '').strip()
                except AttributeError:
                    pass

            # Converting dtw raw into float number
            #
            half_DTW = '½'
            quarter_DTW = '¼'
            three_quarter_DTW = '¾'
            Additional_Number_DTW = 0
            if half_DTW in self.dtwRaw:
                Additional_Number_DTW = 0.5
            if quarter_DTW in self.dtwRaw:
                Additional_Number_DTW = 0.25
            if three_quarter_DTW in self.dtwRaw:
                Additional_Number_DTW = 0.75
            try:
                re.findall(r'\d+', self.dtwRaw)[0]
                self.dtw = float(re.findall(r'\d+', self.dtwRaw)[0]) + Additional_Number_DTW
            except IndexError:
                self.dtw = Additional_Number_DTW
            try:
                re.findall(r'[a-zA-Z]+', self.dtwRaw)[0]
                self.dtw = 0.25
            except IndexError:
                pass

            if self.possition == 0:
                self.dtw = 1000
            if self.possition == 2:
                self.winningDistance = self.dtw
            if self.possition == 1:
                self.dtw = 0

            # Second Item will provide: horseName, SP, favourite, jockey and trainer
            # horseName
            self.horseNameTrimmed = row.find('a', class_='rp-horseTable__horse__name ui-link ui-link_table js-popupLink').text.split('\n')[1].strip().replace("'", "")

            try:
                country = row.find('span', class_='rp-horseTable__horse__country').text.strip()
            except:
                country = ''
            if country != '':
                self.horseName = f'{self.horseNameTrimmed} {country}'
            else:
                self.horseName = self.horseNameTrimmed
            try:
                self.horseID = self.getRowItemByCss(2, row).find('a',
                                                                 class_='rp-horseTable__horse__name ui-link ui-link_table js-popupLink').get(
                    'href').split('/')[3]
            except:
                pass

            # Owner and owner ID

            try:
                owner_href = row.select_one('a[data-test-selector="link-silk"]').get('href')
                self.ownerID = owner_href.split('/')[3]
                self.owner = owner_href.split('/')[4]
            except AttributeError:
                pass

            # SP
            SP_raw = row.find('span', class_='rp-horseTable__horse__price').text.strip()
            try:
                self.SP = 1 + float(re.findall(r'\d+', SP_raw)[0]) / float(re.findall(r'\d+', SP_raw)[1])
            except IndexError:
                self.SP = 2
            # favourite and minimal SP
            self.favourite = ''

            for fav in ['F', 'J', 'C']:
                if fav in SP_raw:
                    self.favourite = fav

            # jockey

            jockey_html = row.select_one('span[data-prefix="J:"]')
            try:
                self.jockey = jockey_html.text.split('\n')[2].strip()
            except IndexError:
                pass
            # jockeyClaim
            try:
                self.jockeyClaim = jockey_html.text.split('\n')[5].strip()
            except IndexError:
                pass

            try:
                self.jockeyID = jockey_html.find('a').get('href').split('/')[3]
            except AttributeError:
                pass

            # trainer

            trainer_html = row.select_one('span[data-prefix="T:"]')

            try:
                self.trainer = trainer_html.text.split('\n')[2].strip()
            except IndexError:
                pass

            try:
                self.trainerID = trainer_html.find('a').get('href').split('/')[3]
            except (IndexError, AttributeError):
                pass

            html = self.getRowItemByCss(5, row)
            try:
                self.weight = 14 * int(html.select_one('span.rp-horseTable__st').text.strip()) + int(
                    html.select_one('span:nth-child(2)').text.strip())
            except ValueError:
                pass

            self.HG = self.fetchElementIfExsists(html, 'span', 'rp-horseTable__headGear')
            self.WS = self.fetchElementIfExsists(html, 'span', 'rp-horseTable__windOperations')
            self.age = self.getRowItemByCss(4, row).text.strip()
            try:
                self.OR = int(self.getRowItemByCss(6, row).text.strip())
            except ValueError:
                self.OR = ''

            self.comment = self.commentRows[index].text.strip()

            pedigreeRow = self.pedigreeRows[index].text.strip()
            self.hColour = pedigreeRow.split('\n')[0].strip().split(' ')[0]
            self.hType = pedigreeRow.split('\n')[0].strip().split(' ')[1]
            self.sire = pedigreeRow.split('\n')[1].strip().replace('               ', '').replace("'", "")
            self.dam = pedigreeRow.split('\n')[6].strip().replace('               ', '').replace("'", "")
            try:
                self.damsSire = pedigreeRow.split('\n')[12].strip().replace('               ', '').replace("'", "").replace(
                    '(', '').replace(')', '')
            except IndexError:
                self.damsSire = 'NOT AVAILABLE'

            extraData = row.find('span', class_='rp-horseTable__extraData')
            if len(extraData.find_all('span')) >= 2:
                try:
                    self.outOfHandicap = extraData.select_one('span:nth-child(4)').text.strip()
                except AttributeError:
                    pass
                try:
                    self.extraWeight = extraData.select_one('span:nth-child(2)').text.strip()

                except AttributeError:
                    pass
            else:
                self.outOfHandicap = self.extraDataHandling('Out-of-Handicaps', extraData)
                self.extraWeight = self.extraDataHandling('Extra-Weights', extraData)

            current_data = self.__dict__.copy()
            current_data.pop('tableHtml', None)
            current_data.pop('tbodyHtml', None)
            current_data.pop('theadHtml', None)
            current_data.pop('mainRows', None)
            current_data.pop('commentRows', None)
            current_data.pop('data', None)
            current_data.pop('pedigreeRows', None)
            self.data.append(current_data)

