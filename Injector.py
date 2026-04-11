from database.DBConnection import DbConnection
from Selenium.LinkCollector import *

if __name__ == '__main__':
    obj = DbConnection('mssql')
    obj.createConnection("AUTOCOMMIT")
    con = obj.connection

    resultStartDate = '2026-04-10'
    resultEndDate = '2026-04-10'
    RaceCardDate = '2026-04-11'

    obj.executeQuery('delete from Race_Card_turf_handicap')

    [DbConnection.importToTable('Race_Card_turf_handicap', con, raceCardFrame(raceCard)) for raceCard in pickRaceCards(f'https://www.racingpost.com/racecards/{RaceCardDate}/')]
    [DbConnection.importToTable('test_table ', con, frameResults(link)) for link in getRaceLinks(DateList(resultStartDate, resultEndDate))]

    obj.executeQuery('insert into racing_post_results select * from test_table')
    obj.executeQuery('delete from test_table')
