

class Table(object):
    def __init__(self, BSimport, classname = 'rp-horseTable__table'):

        self.tableHtml = BSimport.find('table', class_=classname)
        self.tbodyHtml = self.tableHtml.find('tbody')
        self.theadHtml = self.tableHtml.find('thead')
        self.mainRows = []
        self.commentRows = []
        self.pedigreeRows = []

    def getRowsByClassName(self,  cname):
        rows = self.tbodyHtml.find_all('tr', class_=cname)
        return rows

    def getRows(self):
        self.mainRows = self.getRowsByClassName('rp-horseTable__mainRow')
        self.commentRows = self.getRowsByClassName('rp-horseTable__commentRow')
        self.pedigreeRows = self.getRowsByClassName('rp-horseTable__pedigreeRow')

    @staticmethod
    def getRowItemByCss(i, rowHtml):
        return rowHtml.select_one(f'td:nth-child({i})')

    @staticmethod
    def fetchElementIfExsists(inputHtml, tag, cname):
        try:
            element = inputHtml.find(tag, class_=cname).text.strip()
        except AttributeError:
            element = ''
        return element

    @staticmethod
    def extraDataHandling(string, inputHtml):
        extraDataString =''
        try:
            if string in inputHtml.find('img')['alt']:
                extraDataString =  inputHtml.text.strip()
            else:
                pass
        except TypeError:
            pass
        return extraDataString
