import datetime
import pandas as pd
import sys
import time
import re
import openpyxl
from database.DBConnection import DbConnection





def takeRaceCardDate():
    if int(time.strftime("%H", time.localtime())) > 14:
        Current_Date = datetime.date.today() + datetime.timedelta(days=1)
    else:
        Current_Date = datetime.date.today()
    return Current_Date



def checkForParameters(value, column):

    string = column + f" = '{value}'"
    try:
        string = column + '=' + str(float(value))
        return string
    except ValueError:
        pass

    if value == 'ZERO':
        string = column + '=0'
        return string
    if value == 'blanks' and column == 'HG':
        string = "HG is Null"
        return string
    if 'Blanks or ' in value:
        string = f"({column} is null or {column} = {re.findall(r'\d+', value)[0]})"

    if value == 'is not null':
        string = f'{column} is not null'

    if value == 'is null':
        string = f'{column} is null'

    if value == '!=1':
        string = f'{column} !=1'

    if column == 'track' or column == 'hType' or column == 'HG' or column == 'trainer' or column == 'Month':
        if ',' in value:
            values = re.split(',', value)
            string = f'{column} in ('
            for val in values:
                string += f"'{val.strip()}',"
            string = string[:-1]
            string += ')'
        else:
            string = column + f" = '{value}'"
    if '>' in str(value) or '<' in str(value) or 'in (' in str(value):
        string = column + f' {value}'
    if 'between' in str(value):
        string = column + f' {value}'
    if column == 'raceName' or column == 'Last_Race_Name':
        string = column + f' {value}'
    if 'not like' in value:
        string = column + f' {value}'
    return string


if __name__ == '__main__':
    tomorrow = takeRaceCardDate()
    conObj = DbConnection('mssql')
    conObj.createConnection("AUTOCOMMIT")
    con = conObj.connection

    System_file = pd.read_excel('Sistemi_sablon_radni.xlsx').fillna(0)
    for ind in System_file.index:
        where_clause = 'where 1=1 '
        for column in System_file.columns:
            if column == 'System' or column == 'Kvota':
                continue
            if System_file[column][ind]:
                where_clause += f'and {checkForParameters(System_file[column][ind], column)} '

        sql = f"select distinct Track,HorseName,RaceDate,SP,Trainer,profit_SP,'{System_file['System'][ind]}', Jockey, dtw, winningDistance from Turf_2026 "+where_clause + "Order by RaceDate"

        try:
            result = pd.read_sql(sql=sql, con=con)
        except Exception as e:
            print(f'Error in: {sql}')
            print(e)


        result.to_csv(rf"d:\Konji\Exporti_Turf_2026\{System_file['System'][ind]}.csv", index=False)

