from database.DBConnection import DbConnection
from Selenium.LinkCollector import *
from Selenium.NonRunners import *
import time
if __name__ == '__main__':
    obj = DbConnection('mssql')
    obj.createConnection("AUTOCOMMIT")
    con = obj.connection

    resultStartDate = '2026-05-14'  # select max(raceDate) from racing_post_results + 1
    resultEndDate = '2026-05-14'    # pick from a function
    RaceCardDate = '2026-05-15'     # pick from a function

    obj.executeQuery('delete from Race_Card_turf_handicap')

    [DbConnection.importToTable('Race_Card_turf_handicap', con, raceCardFrame(raceCard)) for raceCard in
     pickRaceCards(f'https://www.racingpost.com/racecards/{RaceCardDate}/')]
    print('Race Card imported')
    [DbConnection.importToTable('test_table ', con, frameResults(link)) for link in
     getRaceLinks(DateList(resultStartDate, resultEndDate))]

    obj.executeQuery('insert into racing_post_results select * from test_table')
    obj.executeQuery('delete from test_table')
    print('Results imported')
    # This part should go to another script and be connected with non-runners

    start = time.perf_counter()

    obj.executeQuery(BHANonRunners())
    obj.executeQuery(RPNonRunners())
    obj.executeQuery('exec Populate_Overall_MinOR_FTC')
    obj.executeQuery('exec Populate_OR_Class_L5')
    obj.executeQuery('exec PRB2_Procedure')
    obj.executeQuery('exec MedianOR_Prep_procedure')
    obj.executeQuery('exec CD_Calculations_Procedure')
    obj.executeQuery('exec Race_Card_enrich')

    duration = time.perf_counter() - start

    print(f"NR Update took {duration:.4f} seconds")
