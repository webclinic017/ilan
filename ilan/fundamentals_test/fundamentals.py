import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from files_and_paths import symbols_file
from config import PE_PASS_CRITERIA


def get_fundamentals(symbols_list):
    symbol_df = pd.read_csv(symbols_file)
    fundamentals_df = symbol_df[symbol_df['symbol'].isin(symbols_list)][['symbol', 'name', 'pe_ratio', 'avg_volume',
                                                                         'market_cap']]
    fundamentals_df = fundamentals_df.rename(columns={'symbol': 'ticker'})
    fundamentals_df['market_cap_class'] = fundamentals_df['market_cap'].apply(lambda x: get_mcap_class(x))
    fundamentals_df['pe_ratio'] = fundamentals_df['pe_ratio'].str.replace(',', '').astype(float).fillna(10000)
    fundamentals_df['fundamentals_pe_result'] = np.where(fundamentals_df['pe_ratio'] <= PE_PASS_CRITERIA, 'PASS', 'FAIL')
    fundamentals_df['fundamentals_pe_result'] = np.where(fundamentals_df['pe_ratio'] == 10000, 'PASS',
                                                         fundamentals_df['fundamentals_pe_result'])
    return fundamentals_df


def get_fundamentals_from_mw(symbols_list):
    master_fundamentals = dict()
    i = 1
    for symbol in symbols_list:
        try:
            print(f" {i} Getting fundamentals for : {symbol}")
            fundamental = get_fundamentals_for_symbol(symbol)
            master_fundamentals[symbol] = fundamental.copy()
            i = i + 1
        except:
            print(f"Exception for fundamentals : {symbol}")
            continue
    fundamentals_df = pd.DataFrame(master_fundamentals).transpose().reset_index().rename(columns={'index': 'ticker'})
    fundamentals_df['fundamentals_pe_result'] = np.where(fundamentals_df['pe'] <= 17, 'PASS', 'FAIL')
    fundamentals_df['fundamentals_pe_result'] = np.where(fundamentals_df['pe'] == 10000, 'PASS',
                                                         fundamentals_df['fundamentals_pe_result'])
    return fundamentals_df


def get_fundamentals_for_symbol(symbol):
    url = f'https://www.marketwatch.com/investing/stock/{symbol.lower()}?mod=mw_quote_tab'
    try:
        r = requests.get(url=url)
        html_soup = BeautifulSoup(r.text, 'html.parser')
        data_response = html_soup.find_all('span', attrs={'class':'primary'})
        PE_RATIO = data_response[14].text.strip()
        MARKET_CAP = data_response[9].text.strip()
        MARKET_CAP = clean_volume(MARKET_CAP)
        try:
            PE_RATIO = float(PE_RATIO)
        except:
            PE_RATIO = 10000
        if MARKET_CAP <= 300000000:
            market_cap_class = 'micro'
        elif MARKET_CAP <= 2000000000:
            market_cap_class = 'small'
        elif MARKET_CAP <= 10000000000:
            market_cap_class = 'mid'
        else:
            market_cap_class = 'large'
        data = {'pe': PE_RATIO, 'market_cap': MARKET_CAP, 'market_cap_class': market_cap_class}
        return data.copy()
    except:
        return {'pe': 10000, 'market_cap': 0, 'market_cap_class': 'NA'}


def clean_volume(x):
    x = str(x).replace(',', '')
    x = str(x).replace('$', '')
    if 'M' in x:
        return float(x.split('M')[0]) * 1000000
    elif 'B' in x:
        return float(x.split('B')[0]) * 1000000000
    elif 'T' in x:
        return float(x.split('T')[0]) * 1000000000000
    return np.int64(x)


def get_mcap_class(x):
    if x <= 300000000:
        market_cap_class = 'micro'
    elif x <= 2000000000:
        market_cap_class = 'small'
    elif x <= 10000000000:
        market_cap_class = 'mid'
    else:
        market_cap_class = 'large'
    return market_cap_class
