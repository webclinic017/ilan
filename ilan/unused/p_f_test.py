"""
https://www.psg.co.za/support/tutorials/tutorial-10-point-and-figure-charts
"""

from yahoo_finance_api import yahoo_ohlc_downloader as ohlc_download


import numpy as np
import pandas as pd
import datetime
reversal_points = 3
blocks = np.concatenate((np.arange(0, 5, 0.25),
                         np.arange(5, 20, 0.5),
                         np.arange(20, 100, 1),
                         np.arange(100, 200, 2),
                         np.arange(200, 300, 4)))


data = ohlc_download.download_ohlc(symbol='CRM', from_date='05/01/2020', to_date='17/02/2021')
close = 'close'


def near(x):
    for i in range(0, len(blocks)):
        if blocks[i] <= x < blocks[i+1]:
            return blocks[i]


def fill_df_below(df, col, price):
    loc = np.where(blocks == price)[0][0]
    df.loc[loc - 1, col] = 'X'
    df.loc[loc - 2, col] = 'X'


def n_blocks_below(price):
    if (price == 0) or (price == 1000000):
        return price
    loc = np.where(blocks == price)[0][0]
    return blocks[loc-reversal_points]


def n_blocks_above(price):
    if (price == 0) or (price == 1000000):
        return price
    loc = np.where(blocks == price)[0][0]
    return blocks[loc+reversal_points]


pf_df = pd.DataFrame(index=np.flip(blocks))
pf_df['col1'] = ''
curr_col = 'col1'
mode = 'X'
pf_df.loc[near(data[close].iloc[0]), 'col1'] = mode

curr_high = 0
curr_low = 1000000
recent_x = near(data[close].iloc[0])
recent_o = near(data[close].iloc[0])
ohlc_list = data.to_dict('records')[1:]
s = datetime.datetime.now()
for this_ohlc in ohlc_list:
    if mode == 'X':
        if near(this_ohlc[close]) > n_blocks_below(curr_high):
            if near(this_ohlc[close]) > recent_x:
                pf_df.loc[near(this_ohlc[close]), curr_col] = 'X'
                print(f"{curr_col} : {near(this_ohlc[close])} : X : {this_ohlc[close]}")
                recent_x = near(this_ohlc[close])
            curr_high = max(curr_high, near(this_ohlc[close]))
        else:
            in_list = pf_df[pf_df[curr_col] == 'X'][curr_col].index
            pf_df.loc[in_list[0]:in_list[-1], curr_col] = 'X'
            new_col = 'col' + str(int(curr_col.split('col')[1]) + 1)
            curr_col = new_col
            pf_df[curr_col] = ''
            mode = 'O'
            pf_df.loc[near(this_ohlc[close]), curr_col] = 'O'
            loc = np.where(blocks == near(recent_x))[0][0]
            pf_df.loc[blocks[loc - 1], curr_col] = 'O'
            pf_df.loc[blocks[loc - 2], curr_col] = 'O'
            print(f"{curr_col} : {near(this_ohlc[close])} : O new : {this_ohlc[close]}")
            recent_x = near(this_ohlc[close])
            recent_o = near(this_ohlc[close])
            curr_high = 0
            curr_low = 1000000
    elif mode == 'O':
        if near(this_ohlc[close]) < n_blocks_above(curr_low):
            if near(this_ohlc[close]) < recent_o:
                pf_df.loc[near(this_ohlc[close]), curr_col] = 'O'
                print(f"{curr_col} : {near(this_ohlc[close])} : O : {this_ohlc[close]}")
                recent_o = near(this_ohlc[close])
            curr_low = min(curr_low, near(this_ohlc[close]))
        else:
            in_list = pf_df[pf_df[curr_col] == 'O'][curr_col].index
            pf_df.loc[in_list[0]:in_list[-1], curr_col] = 'O'
            new_col = 'col' + str(int(curr_col.split('col')[1]) + 1)
            curr_col = new_col
            pf_df[curr_col] = ''
            mode = 'X'
            pf_df.loc[near(this_ohlc[close]), curr_col] = 'X'
            loc = np.where(blocks == near(recent_o))[0][0]
            pf_df.loc[blocks[loc + 1], curr_col] = 'X'
            pf_df.loc[blocks[loc + 2], curr_col] = 'X'
            print(f"{curr_col} : {near(this_ohlc[close])} : X new : {this_ohlc[close]}")
            recent_x = near(this_ohlc[close])
            recent_o = near(this_ohlc[close])
            curr_high = 0
            curr_low = 1000000
in_list = pf_df[pf_df[curr_col] == mode][curr_col].index
pf_df.loc[in_list[0]:in_list[-1], curr_col] = mode

pf_df = pf_df.shift(-1)
print(datetime.datetime.now() - s)
