import pandas as pd
import numpy as np


def DateList(startDate, endDate):
    Dates = [str(Date.strftime('%Y-%m-%d')) for Date in
             pd.date_range(start=f'{startDate}', end=f'{endDate}').to_pydatetime().tolist()]
    return Dates
