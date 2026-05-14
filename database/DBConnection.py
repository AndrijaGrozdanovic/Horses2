from config.parameters import Parameters
from sqlalchemy import create_engine, text
from DataFrame.ResultsDataframe import import_csv_folder
import logging
import pandas as pd


class DbConnection(object):
    par = Parameters()

    def __init__(self, dbType):
        self.connectionString = ''
        if dbType == 'mssql':
            self.connectionString = f'mssql://@{self.par.server}/{self.par.database}?driver={self.par.dbdriver}'

        # if dbType == 'postgresql':
        #     self.connectionString = f'postgresql://{self.obj.pguser}:{self.obj.pgpass}@{self.obj.pghost}:{self.obj.pgport}/{self.obj.pgdatabase}'
        self.connection = ''

    def createConnection(self, isoLvl="REPEATABLE READ"):
        try:
            engine = create_engine(self.connectionString, pool_size=10, max_overflow=20, pool_timeout=30,
                                   pool_recycle=3600, fast_executemany=True)
            self.connection = engine.connect().execution_options(isolation_level=isoLvl)
        except Exception as e:
            raise Exception(f"DB does not exist or connection failed: {e}")

    def executeQuery(self, sql):
        return self.connection.execute(text(sql))

    def deleteFromTableIfExsists(self, tableName):
        sql = f"IF OBJECT_ID('dbo.{tableName}', 'U') IS NOT NULL BEGIN DELETE FROM dbo.{tableName}; END"
        self.connection.execute(text(sql))

    @classmethod
    def importToTable(cls, tableName, connection, df):
        df.to_sql(tableName, con=connection, if_exists="append", index=False)


if __name__ == '__main__':
    obj = DbConnection('mssql')
    obj.createConnection("AUTOCOMMIT")
    con = obj.connection
    # df = pd.read_csv(r'd:\failed.csv')
    # df.to_sql('testTable', con, if_exists="append", index=False)

    import_csv_folder(r'd:\SeleniumDrop\\', con, 'racing_post_results')
