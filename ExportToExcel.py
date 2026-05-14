import polars as pl
from database.DBConnection import DbConnection
import xlsxwriter
obj = DbConnection('mssql')
obj.createConnection("AUTOCOMMIT")
con = obj.connection

query = """SELECT * FROM Turf_2026 where YEAR(raceDate) >= 2018 ORDER BY raceDate, raceID"""

# Read from SQL into a Polars DataFrame
df = pl.read_database(query=query, connection=con)
print('Database loaded')
# Export to Excel
df.write_csv(r'd:\Konji\Export_2018_2026.csv', separator='\t')

