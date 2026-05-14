import os
import glob
import pandas as pd
import openpyxl
from openpyxl.styles import Border, Side


def mergeExcel():

    os.chdir(rf'd:\Konji\Exporti_Turf_2026\\')
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    # sortedExcel = combined_csv.sort_values(by=['raceDate', 'raceTime', 'runnerID'])
    combined_csv.to_csv('d:\\Statistika2026.csv', index=False)


mergeExcel()
