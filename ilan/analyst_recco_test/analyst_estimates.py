import requests
from bs4 import BeautifulSoup
import pandas as pd
from config import *
import numpy as np


def get_analyst_estimates(symbols_list):
    master_estimates = dict()
    i = 1
    for symbol in symbols_list:
        try:
            print(f" {i} Getting analyst estimates for : {symbol}")
            estimates = get_analyst_estimates_for_symbol(symbol)
            master_estimates[symbol] = estimates.copy()
            i = i + 1
        except:
            print(f"Exception for analyst estimates : {symbol}")
            continue
    estimates_df = pd.DataFrame(master_estimates).transpose()
    estimates_df = estimates_df.fillna(0)
    estimates_df = estimates_df.replace('N/A', 0)
    estimates_df = estimates_df.astype(int)
    estimates_df = estimates_df.reset_index().rename(columns={'index': 'ticker'})
    estimates_df['3m_perc'] = estimates_df[['3m_buy', '3m_overweight']].astype(int).sum(axis=1) / \
                              estimates_df[[i for i in estimates_df.columns if '3m_' in i]].astype(int).sum(axis=1)
    estimates_df['1m_perc'] = estimates_df[['1m_buy', '1m_overweight']].astype(int).sum(axis=1) / \
                              estimates_df[[i for i in estimates_df.columns if '1m_' in i]].astype(int).sum(axis=1)
    estimates_df['curr_perc'] = estimates_df[['curr_buy', 'curr_overweight']].astype(int).sum(axis=1) / \
                              estimates_df[[i for i in estimates_df.columns if 'curr_' in i]].astype(int).sum(axis=1)
    estimates_df['analyst_result'] = np.where((estimates_df['3m_perc'] > ANALYST_PASS_CRITERIA) &
                                              (estimates_df['1m_perc'] > ANALYST_PASS_CRITERIA) &
                                              (estimates_df['curr_perc'] > ANALYST_PASS_CRITERIA), 'PASS', 'FAIL')
    return estimates_df.fillna(0)


def get_analyst_estimates_for_symbol(symbol):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'}
    symbol = str(symbol).replace('-', '.')
    url = f'https://www.marketwatch.com/investing/stock/{symbol.lower()}/analystestimates?mod=mw_quote_tab'
    try:
        r = requests.get(url=url, headers=headers, timeout=10)
        html_soup = BeautifulSoup(r.text, 'html.parser')
        data_response = html_soup.find_all('div', attrs={'class': 'bar-chart'})
        if len(data_response) == 0:
            return
        Buy_3M_AGO = data_response[0].text.strip()
        Buy_1M_AGO = data_response[1].text.strip()
        Buy_CURRENT = data_response[2].text.strip()

        Overweight_3M_AGO = data_response[3].text.strip()
        Overweight_1M_AGO = data_response[4].text.strip()
        Overweight_CURRENT = data_response[5].text.strip()

        Hold_3M_AGO = data_response[6].text.strip()
        Hold_1M_AGO = data_response[7].text.strip()
        Hold_CURRENT = data_response[8].text.strip()

        Underweight_3M_AGO = data_response[9].text.strip()
        Underweight_1M_AGO = data_response[10].text.strip()
        Underweight_CURRENT = data_response[11].text.strip()

        Sell_3M_AGO = data_response[12].text.strip()
        Sell_1M_AGO = data_response[13].text.strip()
        Sell_CURRENT = data_response[14].text.strip()

        data = {'3m_buy': Buy_3M_AGO, '3m_overweight': Overweight_3M_AGO, '3m_hold': Hold_3M_AGO,
                '3m_underweight': Underweight_3M_AGO, '3m_sell': Sell_3M_AGO,
                '1m_buy': Buy_1M_AGO, '1m_overweight': Overweight_1M_AGO, '1m_hold': Hold_1M_AGO,
                '1m_underweight': Underweight_1M_AGO, '1m_sell': Sell_1M_AGO,
                'curr_buy': Buy_CURRENT, 'curr_overweight': Overweight_CURRENT, 'curr_hold': Hold_CURRENT,
                'curr_underweight': Underweight_CURRENT, 'curr_sell': Sell_CURRENT}
        return data.copy()
    except requests.exceptions.Timeout as exc:
        print(f'TimeOut exception for {symbol}')
        return dict()
    except:
        print(f'Exception for {symbol}')
        return dict()


def get_analyst_estimates_for_symbol_old(symbol):
    url = f'https://www.marketwatch.com/investing/stock/{symbol.lower()}/analystestimates?mod=mw_quote_tab'
    r = requests.get(url=url)
    html_soup = BeautifulSoup(r.text, 'html.parser')
    data_response = html_soup.find_all('div', attrs={'class': 'bar-chart'})

    Buy_3M_AGO = data_response[0].text.strip()
    Buy_1M_AGO = data_response[1].text.strip()
    Buy_CURRENT = data_response[2].text.strip()

    Overweight_3M_AGO = data_response[3].text.strip()
    Overweight_1M_AGO = data_response[4].text.strip()
    Overweight_CURRENT = data_response[5].text.strip()

    Hold_3M_AGO = data_response[6].text.strip()
    Hold_1M_AGO = data_response[7].text.strip()
    Hold_CURRENT = data_response[8].text.strip()

    Underweight_3M_AGO = data_response[9].text.strip()
    Underweight_1M_AGO = data_response[10].text.strip()
    Underweight_CURRENT = data_response[11].text.strip()

    Sell_3M_AGO = data_response[12].text.strip()
    Sell_1M_AGO = data_response[13].text.strip()
    Sell_CURRENT = data_response[14].text.strip()

    data = {'3m_buy': Buy_3M_AGO, '3m_overweight': Overweight_3M_AGO, '3m_hold': Hold_3M_AGO,
            '3m_underweight': Underweight_3M_AGO, '3m_sell': Sell_3M_AGO,
            '1m_buy': Buy_1M_AGO, '1m_overweight': Overweight_1M_AGO, '1m_hold': Hold_1M_AGO,
            '1m_underweight': Underweight_1M_AGO, '1m_sell': Sell_1M_AGO,
            'curr_buy': Buy_CURRENT, 'curr_overweight': Overweight_CURRENT, 'curr_hold': Hold_CURRENT,
            'curr_underweight': Underweight_CURRENT, 'curr_sell': Sell_CURRENT}

    return data.copy()

