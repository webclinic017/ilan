import datetime
import pandas as pd
from config import *


def get_next_eod_run_time():
    today = pd.to_datetime(datetime.datetime.utcnow())
    dates = [datetime.datetime.combine(i, eod_run_time_utc)
             for i in pd.date_range('1/1/2020', '31/12/2099')]
    week_days = [i for i in dates if i.weekday() < 5]
    for i in range(0, len(week_days)-1):
        if week_days[i] < today < week_days[i+1]:
            return week_days[i+1]


def get_symbol_updater_run_time():
    today = pd.to_datetime(datetime.datetime.utcnow())
    dates = [datetime.datetime.combine(i, eod_run_time_utc)
             for i in pd.date_range('1/1/2020', '31/12/2099')]
    saturdays = [i for i in dates if i.weekday() == 5]
    for i in range(0, len(saturdays)-1):
        if saturdays[i] < today < saturdays[i+1]:
            return saturdays[i+1]


def get_next_intraday_run_time():
    ''


