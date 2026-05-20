from DataFrame.ResultsDataframe import frameResults, DateList
from database.DBConnection import DbConnection
from Selenium.LinkCollector import *
from SystemReaderLive import takeRaceCardDate
from rapidapi_racingAPI import get_turf_handicap_racecards
import datetime

if __name__ == '__main__':
    obj = DbConnection('mssql')
    obj.createConnection("AUTOCOMMIT")
    con = obj.connection
    days = takeRaceCardDate()

    maxDate = obj.executeQuery('select max(raceDate) from racing_post_results')
    resultStartDate = maxDate.fetchone()[0] + datetime.timedelta(days=1)
    resultEndDate = days[0] + datetime.timedelta(days=-1)
    obj.executeQuery('delete from Race_Card_turf_handicap')
    get_turf_handicap_racecards(days[1])
    [DbConnection.importToTable('test_table ', con, frameResults(link)) for link in getRaceLinks(DateList(resultStartDate, resultEndDate))]
    obj.executeQuery('insert into racing_post_results select * from test_table')
    obj.executeQuery('delete from test_table')

