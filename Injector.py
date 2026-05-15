from DataFrame.ResultsDataframe import raceCardFrame, frameResults, DateList
from database.DBConnection import DbConnection
from Selenium.LinkCollector import *
from SystemReaderLive import takeRaceCardDate
import datetime

if __name__ == '__main__':
    obj = DbConnection('mssql')
    obj.createConnection("AUTOCOMMIT")
    con = obj.connection

    maxDate = obj.executeQuery('select max(raceDate) from racing_post_results')

    resultStartDate = maxDate.fetchone()[0] + datetime.timedelta(days=1)
    RaceCardDate = takeRaceCardDate()
    resultEndDate = RaceCardDate + datetime.timedelta(days=-1)

    obj.executeQuery('delete from Race_Card_turf_handicap')

    [DbConnection.importToTable('Race_Card_turf_handicap', con, raceCardFrame(raceCard)) for raceCard in
     pickRaceCards(f'https://www.racingpost.com/racecards/{RaceCardDate}/')]
    print('Race Card imported')
    [DbConnection.importToTable('test_table ', con, frameResults(link)) for link in
     getRaceLinks(DateList(resultStartDate, resultEndDate))]

    obj.executeQuery('insert into racing_post_results select * from test_table')
    obj.executeQuery('delete from test_table')
    print('Results imported')
