import re


class RaceCardRunners(object):


    def __init__(self, BSimport):
        self.rowList = BSimport.find_all('div', class_='RC-runnerRow js-RC-runnerRow js-PC-runnerRow')
        self.horseName = ""
        self.horseNameRaw = ""
        self.formUrl = ""
        self.horseID = ""
        self.draw = ""
        self.htype = ""
        self.hcolor = ""
        self.hg = ""
        self.age = ""
        self.weight = ""
        self.OR = ""
        self.jockey = ""
        self.jockeyID = ""
        self.jockeyClaim = ""
        self.trainer = ""
        self.trainerID = ""
        self.owner = ""
        self.ownerID = ""
        self.data = []

    def setParameters(self, row):
        self.horseNameRaw = row.find('a', class_='RC-runnerName ui-link ui-link_table js-popupLink js-bestOddsRunnerHorseName').text.split('\n')[1].strip().replace("'", "")
        horseURL = 'https://www.racingpost.com' + row.find('a', class_='RC-runnerName ui-link ui-link_table js-popupLink js-bestOddsRunnerHorseName').get('href')
        try:
            self.age = int(row.find('span', class_='RC-runnerAge').text.strip())
        except ValueError:
            pass
        try:
            self.formUrl = re.sub(r'#race-id=.*','',str(horseURL).replace('/profile/horse/', '/profile/tab/horse/'))+'/form'

        except TypeError:
            pass
        self.horseID = self.formUrl.split('/')[6]
        try:
            self.draw = re.findall(r'\d+', row.find('span', class_='RC-runnerNumber__draw').text.strip())[0]
        except IndexError:
            pass
        try:
            self.weight = int(row.find('span', class_='RC-runnerWgt__carried').get('data-order-wgt'))
        except ValueError:
            pass
        self.hg = row.find('span', class_='RC-runnerHeadgearCode RC-runnerInfo__name').text.strip()

        jockeyHtml = row.find('div', class_='RC-runnerInfo RC-runnerInfo_jockey').find('a')

        try:
            self.jockey = jockeyHtml.text.split('\n')[1].strip().replace("'", "")
        except AttributeError:
            pass
        self.jockeyClaim = row.find('span', class_='RC-runnerInfo__count').text.strip()
        try:
            self.jockeyID = jockeyHtml.get('href').split('/')[3]
        except (AttributeError, IndexError):
            pass

        trainerHtml = row.find('div', class_='RC-runnerInfo RC-runnerInfo_trainer').find('a')

        self.trainer = trainerHtml.text.split('\n')[1].strip().replace("'", "")
        try:
            self.trainerID = trainerHtml.get('href').split('/')[3]
        except (AttributeError, IndexError):
            pass


        try:
            self.OR = int(row.find('span', class_='RC-runnerOr').text.strip())
        except ValueError:
            pass

        ownerHTML = row.find('div', class_='RC-runnerInfo RC-runnerInfo_owner').find('a')
        # print(ownerHTML.get('href').split('/'))
        try:
            self.owner = ownerHTML.get('href').split('/')[4]
        except (AttributeError, IndexError):
            pass

        try:
            self.ownerID = ownerHTML.get('href').split('/')[3]
        except (AttributeError, IndexError):
            pass

        self.htype = row.find('div', class_='RC-pedigree').find('span').text.strip().split(' ')[-1]
        self.hcolor = row.find('div', class_='RC-pedigree').find('span').text.strip().split(' ')[0]

        current_data = self.__dict__.copy()
        current_data.pop('rowList', None)
        current_data.pop('formUrl', None)
        current_data.pop('data', None)
        self.data.append(current_data)




