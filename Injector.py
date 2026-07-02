from DataFrame.ResultsDataframe import frameResults, DateList
from database.DBConnection import DbConnection
from Selenium.LinkCollector import *
from Selenium.NonRunners import *
from SystemReaderLive import takeRaceCardDate, executeSystemsInProduction
from rapidapi_racingAPI import get_turf_handicap_racecards
import datetime

if __name__ == '__main__':
    obj = DbConnection('mssql')
    obj.createConnection("AUTOCOMMIT")
    con = obj.connection
    days = takeRaceCardDate()

    maxDate = obj.executeQuery('select max(raceDate) from racing_post_results').fetchone()[0]
    resultStartDate = maxDate + datetime.timedelta(days=1)
    resultEndDate = days[0] + datetime.timedelta(days=-1)
    obj.executeQuery('delete from test_table')
    [DbConnection.importToTable('test_table ', con, frameResults(link)) for link in getRaceLinks(DateList(resultStartDate, resultEndDate))]
    obj.executeQuery('insert into racing_post_results select * from test_table')

    obj.executeQuery('delete from Race_Card_turf_handicap')
    get_turf_handicap_racecards(days[1])
    obj.executeQuery(BHANonRunners())

    obj.executeQuery('exec RC_Update_NoOfRunners')
    obj.executeQuery('exec populate_Race_Card_Median_OR')
    obj.executeQuery('exec Populate_Overall_MinOR_FTC')
    obj.executeQuery('exec Populate_OR_Class_L5')
    obj.executeQuery('exec RC_PRB2_Procedure')
    obj.executeQuery('exec MedianOR_Prep_procedure')
    obj.executeQuery('exec CD_Calculations_Procedure')
    obj.executeQuery('exec Race_Card_enrich_new')
    obj.executeQuery('delete from system_evidence')
    executeSystemsInProduction(days[0], con)
