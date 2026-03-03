import os
import glob
import pandas as pd
import openpyxl
from openpyxl.styles import Border, Side


def mergeExcel():

    os.chdir(rf'd:\SeleniumDrop\\')
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    sortedExcel = combined_csv.sort_values(by=['raceDate', 'raceTime', 'runnerID'])
    sortedExcel.to_excel('d:\\NewExport.xlsx', index=False)

mergeExcel()