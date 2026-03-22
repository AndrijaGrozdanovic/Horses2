import pandas as pd
import os
import glob


def merge_csv_string(string):
    os.chdir(rf'd:\Races\{string}\\')
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    sortedExcel = combined_csv.sort_values(by=['raceDate', 'raceTime', 'runnerID'])
    sortedExcel.to_csv(f'd:\\{string}.csv', index=False)


# merge_csv_string('2022')
merge_csv_string('2023')
merge_csv_string('2024')
merge_csv_string('2025')
merge_csv_string('2026')
