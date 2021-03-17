"""
1. Get all tickers
2. options filters:
    - within 2 months
    - oi > 1
    - volume > 1
"""
from yahoo_fin.options import *
from yahoo_fin.stock_info import *
import numpy as np
from config import *


def get_data_for_symbols(symbols_list):
    master_data_df = pd.DataFrame()
    i = 1
    for this_symbol in symbols_list:
        try:
            print(f" {i} Processing options filter for : {this_symbol}")
            this_sym_df = get_call_df_for_symbol(this_symbol)
            # print(len(master_data_df))
            if len(master_data_df) > 0:
                master_data_df = master_data_df.append(this_sym_df, ignore_index=True)
            else:
                master_data_df = this_sym_df
            i = i + 1
        except:
            print(f"Exception for option filters : {this_symbol}")
            continue
        # print(len(master_data_df))
    return master_data_df


def get_call_df_for_symbol(symbol):
    try:
        expiry_dates = get_expiration_dates(symbol)
    except:
        print(f"No options data for {symbol}")
        return pd.DataFrame()

    recent_dates = [pd.to_datetime(i).date() for i in expiry_dates
                    if pd.to_datetime(i) < datetime.today() + timedelta(days=N_RECENT_DAYS)]
    if len(recent_dates) > 0:
        call_df = pd.DataFrame()
        for this_date in recent_dates:
            try:
                options = get_options_chain(ticker=symbol, date=this_date)
                this_call_df = options['calls']
                if len(call_df) > 0:
                    call_df = call_df.append(this_call_df, ignore_index=True)
                else:
                    call_df = this_call_df
            except:
                print(f"No options data for expiry: {this_date}")
                continue

        if len(call_df) > 0:
            call_df.columns = ['symbol', 'recent_trade_date', 'strike_price', 'premium', 'bid', 'ask', 'change',
                               'change_pct', 'volume_str', 'oi_str', 'implied_volatility']
            call_df['premium'] = call_df['premium'].replace('-', np.nan).astype(float).fillna(0)
            call_df['bid'] = call_df['bid'].replace('-', np.nan).astype(float).fillna(0)
            call_df['ask'] = call_df['ask'].replace('-', np.nan).astype(float).fillna(0)
            call_df['strike_price'] = call_df['strike_price'].replace('-', np.nan).astype(float).fillna(0)
            call_df['implied_volatility'] = call_df['implied_volatility'].apply(lambda x: clean_pct(x))
            call_df['change_pct'] = call_df['change_pct'].apply(lambda x: clean_pct(x))
            call_df['ltp'] = call_df['premium']
            call_df['premium'] = np.where((call_df['bid'].astype(float) == 0) &
                                          (call_df['ask'].astype(float) == 0),
                                          call_df['ltp'],
                                          (call_df['bid'].astype(float) + call_df['ask'].astype(float))/2)
            call_df['type'] = 'CALL'
            call_df['expiry_date'] = call_df['symbol'].apply(lambda x: pd.to_datetime(x.split(symbol)[1][0:6],
                                                                                      format='%y%m%d'))
            # call_df = call_df[['type', 'symbol', 'expiry_date', 'strike_price', 'premium', 'bid',
            # 'ask', 'volume_str', 'oi_str']]
            call_df['volume'] = call_df['volume_str'].replace('-', np.nan).fillna(0).apply(lambda x: clean_volume(x))
            call_df['oi'] = call_df['oi_str'].replace('-', np.nan).fillna(0).apply(lambda x: clean_volume(x))
            # call_df = call_df[call_df['volume'] >= MIN_VOLUME]
            # call_df = call_df[call_df['oi'] >= MIN_OI]
            call_df.columns = ['option_' + i for i in call_df.columns]
            call_df['stock_symbol'] = symbol
            try:
                price = get_live_price(symbol)
            except:
                print("Stock price retrieval error")
                return pd.DataFrame()
            call_df['stock_price'] = price
            call_df['last_update_utc_time'] = datetime.utcnow()
            return call_df
    return pd.DataFrame()


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


def clean_pct(x):
    if x == '-':
        x = '0'
    x = str(x).replace(',', '')
    x = str(x).replace('-', '')
    x = str(x).replace('%', '')
    return float(x) / 100

