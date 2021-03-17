from yahoo_finance_api import yahoo_screener_scrapper
from datetime import datetime
import pandas as pd
from files_and_paths import symbols_file
import numpy as np
import os


def download_symbols_list():
    if os.path.isfile(symbols_file):
        os.rename(symbols_file, 'symbol_list_backup/' + symbols_file.split('.csv')[0] + '_' +
                  str(datetime.today().date()).replace('-', '_') + '.csv')
    s = datetime.utcnow()
    yahoo_screener_scrapper.get_data_for_country()
    print(f'Downloaded symbols list. Time taken: {datetime.utcnow()-s}')
    clean_data()


def get_symbols_list():
    df = pd.read_csv(symbols_file)
    if len(df) > 0:
        return df['symbol'].tolist()
    else:
        return list()


def clean_data():
    country_df = pd.read_csv(symbols_file)
    country_df.columns = ['symbol', 'name', 'price', 'chg', 'pct_chg', 'volume_str',
                          'avg_volume_str', 'market_cap_str', 'pe_ratio']
    country_df['avg_volume'] = country_df['avg_volume_str'].fillna('0').apply(lambda x: clean_volume(x)).astype(np.int64)
    country_df['market_cap'] = country_df['market_cap_str'].fillna('0').apply(lambda x: clean_volume(x)).astype(
        np.int64)
    country_df = country_df.sort_values('market_cap', ascending=False)
    country_df.to_csv(symbols_file, index=False)


def clean_volume(x):
    x = str(x).replace(',', '')
    if 'M' in x:
        return float(x.split('M')[0]) * 1000000
    elif 'B' in x:
        return float(x.split('B')[0]) * 1000000000
    elif 'T' in x:
        return float(x.split('T')[0]) * 1000000000000
    return np.int64(x)

