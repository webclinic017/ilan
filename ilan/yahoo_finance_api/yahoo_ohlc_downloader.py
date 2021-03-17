import datetime
from yahoo_fin.stock_info import *


def download_ohlc(symbol, from_date='01/01/2000', to_date='02/01/2099', interval='1d'):
    s = datetime.datetime.now()
    ohlc = get_data(ticker=symbol, start_date=from_date, end_date=to_date, interval=interval)
    return ohlc


def get_us_symbols():
    return tickers_nasdaq()

