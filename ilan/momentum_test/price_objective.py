"""
https://www.psg.co.za/support/tutorials/tutorial-10-point-and-figure-charts
"""

from yahoo_finance_api import yahoo_ohlc_downloader as ohlc_download
import numpy as np
import pandas as pd
from config import *


def get_po_for_symbols(symbols_list):
    master_df_dict = dict()
    master_po_dict = dict()
    i = 1
    for symbol in symbols_list:
        try:
            print(f" {i} Computing price objective for : {symbol}")
            pf_df, po_dict = get_po_for_symbol(symbol)
            master_df_dict[symbol] = pf_df.copy()
            master_po_dict[symbol] = po_dict.copy()
            i = i + 1
        except:
            print(f"Exception for price objective : {symbol}")
            continue
    po_df = pd.DataFrame(master_po_dict).transpose().reset_index().rename(columns={'index': 'ticker'})
    po_df['po_returns'] = (po_df['price_objective'] - po_df['cmp_pf'])/po_df['cmp_pf']
    po_df['pf_result'] = np.where(po_df['po_returns'] >= PF_PASS_CRITERIA, 'PASS', 'FAIL')
    return master_df_dict, po_df

#
# def get_po_for_symbol(symbol):
#     data = ohlc_download.download_ohlc(symbol=symbol, from_date='01/01/2020')
#     close = 'adjclose'
#     high = 'high'
#     low = 'low'
#     max_block = max(int(data['high'].max()) + 50, 300)
#     blocks = np.concatenate((np.arange(0, 5, 0.25),
#                              np.arange(5, 20, 0.5),
#                              np.arange(20, 100, 1),
#                              np.arange(100, 200, 2),
#                              np.arange(200, max_block, 4)))
#
#     def near(x):
#         for i in range(0, len(blocks)):
#             if blocks[i] <= x < blocks[i+1]:
#                 return blocks[i]
#
#     def hnear(x):
#         for i in range(0, len(blocks)):
#             if blocks[i] <= x < blocks[i+1]:
#                 return blocks[i]
#
#     def lnear(x):
#         for i in range(0, len(blocks)):
#             if blocks[i - 1] <= x < blocks[i]:
#                 return blocks[i]
#
#     def n_blocks_below(price):
#         if (price == 0) or (price == 1000000):
#             return price
#         loc = np.where(blocks == price)[0][0]
#         return blocks[loc-PF_REVERSAL_POINTS]
#
#     def n_blocks_above(price):
#         if (price == 0) or (price == 1000000):
#             return price
#         loc = np.where(blocks == price)[0][0]
#         return blocks[loc+PF_REVERSAL_POINTS]
#
#     pf_df = pd.DataFrame(index=np.flip(blocks))
#     pf_df['col1'] = ''
#     curr_col = 'col1'
#     mode = 'X'
#     pf_df.loc[hnear(data[high].iloc[0]), 'col1'] = mode
#     data['date'] = data.index
#     curr_high = 0
#     curr_low = 1000000
#     recent_x = hnear(data[high].iloc[0])
#     recent_o = lnear(data[low].iloc[0])
#     ohlc_list = data.to_dict('records')[1:]
#     s = datetime.now()
#     for this_ohlc in ohlc_list:
#         if mode == 'X':
#             print(f"{this_ohlc['date']} curr_high {curr_high}: n_blocks_below(curr_high): {n_blocks_below(curr_high)}")
#             # TODO: CHECK THIS and ELIF LOGIC
#             if hnear(this_ohlc[high]) > n_blocks_below(curr_high) and not (this_ohlc[low] < n_blocks_below(curr_high)):
#                 if hnear(this_ohlc[high]) > recent_x:
#                     pf_df.loc[hnear(this_ohlc[high]), curr_col] = 'X'
#                     print(f"{curr_col} {this_ohlc['date']} : {hnear(this_ohlc[high])} : X : {this_ohlc[high]}")
#                     recent_x = hnear(this_ohlc[high])
#                 curr_high = max(curr_high, hnear(this_ohlc[high]))
#             elif this_ohlc[low] < n_blocks_below(curr_high): # TODO
#                 print(f"{this_ohlc['date']} curr_low {curr_low}: n_blocks_above(curr_low): {n_blocks_above(curr_low)}")
#                 in_list = pf_df[pf_df[curr_col] == 'X'][curr_col].index
#                 pf_df.loc[in_list[0]:in_list[-1], curr_col] = 'X'
#                 print(f"{curr_col} {this_ohlc['date']}  : {in_list[0]} : {in_list[-1]} : X add: {this_ohlc[high]}")
#                 # print(pf_df[pf_df[curr_col] == 'X'])
#                 new_col = 'col' + str(int(curr_col.split('col')[1]) + 1)
#                 curr_col = new_col
#                 pf_df[curr_col] = ''
#                 mode = 'O'
#                 pf_df.loc[lnear(this_ohlc[low]), curr_col] = 'O'
#                 loc = np.where(blocks == recent_x)[0][0]
#                 pf_df.loc[blocks[loc - 1], curr_col] = 'O'
#                 pf_df.loc[blocks[loc - 2], curr_col] = 'O'
#                 print(f"{curr_col} {this_ohlc['date']}  : {lnear(this_ohlc[low])} : O new : {this_ohlc[low]}")
#                 print(f"{curr_col} {this_ohlc['date']}  : {blocks[loc - 1]} : O fill 1: {this_ohlc[low]}")
#                 print(f"{curr_col} {this_ohlc['date']} : {blocks[loc - 2]} : O fill 2: {this_ohlc[low]}")
#                 # recent_x = lnear(this_ohlc[low])
#                 recent_o = lnear(this_ohlc[low])
#                 curr_high = 0
#                 curr_low = 1000000
#         elif mode == 'O':
#             print(f"{this_ohlc['date']} curr_low {curr_low}: n_blocks_above(curr_low): {n_blocks_above(curr_low)}")
#             # TODO: CHECK THIS and ELIF LOGIC
#             if lnear(this_ohlc[low]) < n_blocks_above(curr_low) and not (this_ohlc[high] > n_blocks_above(curr_low)):
#                 if lnear(this_ohlc[low]) < recent_o:
#                     pf_df.loc[lnear(this_ohlc[low]), curr_col] = 'O'
#                     print(f"{curr_col} {this_ohlc['date']}  : {lnear(this_ohlc[low])} : O : {this_ohlc[low]}")
#                     recent_o = lnear(this_ohlc[low])
#                 curr_low = min(curr_low, lnear(this_ohlc[low]))
#             elif this_ohlc[high] > n_blocks_above(curr_low):
#                 print(f"{this_ohlc['date']} curr_high {curr_high}: n_blocks_below(curr_high): {n_blocks_below(curr_high)}")
#                 in_list = pf_df[pf_df[curr_col] == 'O'][curr_col].index
#                 pf_df.loc[in_list[0]:in_list[-1], curr_col] = 'O'
#                 print(f"{curr_col} {this_ohlc['date']}  : {in_list[0]} : {in_list[-1]} : O add: {this_ohlc[low]}")
#                 new_col = 'col' + str(int(curr_col.split('col')[1]) + 1)
#                 curr_col = new_col
#                 pf_df[curr_col] = ''
#                 mode = 'X'
#                 pf_df.loc[hnear(this_ohlc[high]), curr_col] = 'X'
#                 loc = np.where(blocks == recent_o)[0][0]
#                 pf_df.loc[blocks[loc + 1], curr_col] = 'X'
#                 pf_df.loc[blocks[loc + 2], curr_col] = 'X'
#                 print(f"{curr_col} {this_ohlc['date']}  : {hnear(this_ohlc[high])} : X new : {this_ohlc[high]}")
#                 print(f"{curr_col} {this_ohlc['date']}  : {blocks[loc + 1]} : X fill 1: {this_ohlc[high]}")
#                 print(f"{curr_col} {this_ohlc['date']} : {blocks[loc + 2]} : X fill 2: {this_ohlc[high]}")
#                 recent_x = hnear(this_ohlc[high])
#                 # recent_o = lnear(this_ohlc[low])
#                 curr_high = 0
#                 curr_low = 1000000
#     in_list = pf_df[pf_df[curr_col] == mode][curr_col].index
#     pf_df.loc[in_list[0]:in_list[-1], curr_col] = mode
#
#     # for this_col in pf_df.columns:
#     #     pf_df.loc[pf_df[pf_df[this_col] != ''][this_col].index[-1], this_col] = ''
#
#     po_dict = get_po_new(pf_df)
#     po_dict['cmp_pf'] = data['close'].iloc[-1]
#     return pf_df, po_dict.copy()
#
#
# def get_po(pf_df):
#     po_dict = dict()
#     curr_col_id = -1
#     while True:
#         if abs(curr_col_id) > len(pf_df.columns):
#             po_dict['direction'] = 'NA'
#             po_dict['price_objective'] = 0
#             break
#         last_col = pf_df.columns[curr_col_id]
#         prev_col = 'col' + str(int(last_col.split('col')[1]) - 2)
#         last_mode = 'X' if 'X' in list(pf_df[last_col].unique()) else 'O'
#         if last_mode == 'X':
#             col_ser = pf_df[pf_df[last_col] == last_mode][last_col]
#             if col_ser.index[0] > pf_df[pf_df[prev_col] == last_mode][prev_col].index[0]:
#                 # n = len(col_ser)
#                 o_mul = 3
#                 # box_s = box_size(col_ser.index[0])
#                 # print(f"Bullish : {n} | {o_mul} | {box_s} | {col_ser.index[-1]}")
#                 bs = col_ser.index[0] - col_ser.index[-1] + box_size(col_ser.index[-1])
#                 po = bs * o_mul  + col_ser.index[-1]
#                 # print(f"Price Obj. : {po}")
#                 po_dict['direction'] = 'Bullish'
#                 po_dict['price_objective'] = po
#                 break
#             else:
#                 curr_col_id = curr_col_id - 1
#                 continue
#         elif last_mode == 'O':
#             col_ser = pf_df[pf_df[last_col] == last_mode][last_col]
#             if col_ser.index[-1] < pf_df[pf_df[prev_col] == last_mode][prev_col].index[-1]:
#                 # n = len(col_ser)
#                 o_mul = 2
#                 # box_s = box_size(col_ser.index[0])
#                 # print(f"Bearish : {n} | {o_mul} | {box_s} | {col_ser.index[0]}")
#                 bs = col_ser.index[0] - col_ser.index[-1] + box_size(col_ser.index[-1])
#                 po = col_ser.index[0] - bs * o_mul
#                 # print(f"Price Obj. : {po}")
#                 po_dict['direction'] = 'Bearish'
#                 po_dict['price_objective'] = po
#                 break
#             else:
#                 curr_col_id = curr_col_id - 1
#                 continue
#     return po_dict.copy()
#


def get_po_new(pf_df):
    """"""
    if len(pf_df.columns) < 4:
        po_dict = dict()
        po_dict['direction'] = 'None'
        po_dict['price_objective'] = 0
        return po_dict.copy()
    try:
        signal_dict = dict()
        i = 0
        for this_col in pf_df.columns:
            if i > 1:
                mode = 'X' if 'X' in list(pf_df[this_col].unique()) else 'O'
                prev_col = 'col' + str(int(this_col.split('col')[1]) - 2)
                col_ser = pf_df[pf_df[this_col] == mode][this_col]
                if mode == 'X':
                    if len(pf_df[pf_df[prev_col] == mode][prev_col]) > 0:
                        if col_ser.index[0] > pf_df[pf_df[prev_col] == mode][prev_col].index[0]:
                            signal_dict[this_col] = mode
                else:
                    if len(pf_df[pf_df[prev_col] == mode][prev_col]) > 0:
                        if col_ser.index[-1] < pf_df[pf_df[prev_col] == mode][prev_col].index[-1]:
                            signal_dict[this_col] = mode
            i = i+1

        cols = list(signal_dict.keys())
        recent_signal_col = cols[0]
        recent_sig = signal_dict[recent_signal_col]
        for this_col in cols:
            if recent_sig != signal_dict[this_col]:
                recent_signal_col = this_col
                recent_sig = signal_dict[this_col]
        po_dict = dict()
        col_ser = pf_df[pf_df[recent_signal_col] == recent_sig][recent_signal_col]
        if recent_sig == 'X':
            o_mul = 3
            bs = col_ser.index[0] - col_ser.index[-1] + box_size(col_ser.index[-1])
            po = bs * o_mul + col_ser.index[-1]
            po_dict['direction'] = 'Bullish'
            po_dict['price_objective'] = po
        else:
            o_mul = 2
            bs = col_ser.index[0] - col_ser.index[-1] + box_size(col_ser.index[-1])
            po = col_ser.index[0] - bs * o_mul
            po_dict['direction'] = 'Bearish'
            po_dict['price_objective'] = po
        return po_dict.copy()
    except:
        po_dict = dict()
        po_dict['direction'] = 'None'
        po_dict['price_objective'] = 0
        return po_dict.copy()


def box_size(x):
    if x < 5:
        return 0.25
    elif x < 20:
        return 0.5
    elif x < 100:
        return 1
    elif x < 200:
        return 2
    else:
        return 4


#
# def get_po_for_symbol_new(symbol):
#     data = ohlc_download.download_ohlc(symbol=symbol, from_date='01/01/2020')
#     close = 'adjclose'
#     high = 'high'
#     low = 'low'
#     max_block = max(int(data['high'].max()) + 50, 300)
#     blocks = np.concatenate((np.arange(0, 5, 0.25),
#                              np.arange(5, 20, 0.5),
#                              np.arange(20, 100, 1),
#                              np.arange(100, 200, 2),
#                              np.arange(200, max_block, 4)))
#
#     def near(x):
#         for i in range(0, len(blocks)):
#             if blocks[i] <= x < blocks[i+1]:
#                 return blocks[i]
#
#     def hnear(x):
#         for i in range(0, len(blocks)):
#             if blocks[i] <= x < blocks[i+1]:
#                 return blocks[i]
#
#     def lnear(x):
#         for i in range(0, len(blocks)):
#             if blocks[i - 1] <= x < blocks[i]:
#                 return blocks[i]
#
#     def n_blocks_below(price):
#         if (price == 0) or (price == 1000000):
#             return price
#         loc = np.where(blocks == price)[0][0]
#         return blocks[loc-PF_REVERSAL_POINTS]
#
#     def n_blocks_above(price):
#         if (price == 0) or (price == 1000000):
#             return price
#         loc = np.where(blocks == price)[0][0]
#         return blocks[loc+PF_REVERSAL_POINTS]
#
#     pf_df = pd.DataFrame(index=np.flip(blocks))
#     pf_df['col1'] = ''
#     curr_col = 'col1'
#     mode = 'X'
#     pf_df.loc[hnear(data[high].iloc[0]), 'col1'] = mode
#     data['date'] = data.index
#     curr_high = 0
#     curr_low = 1000000
#     recent_x = hnear(data[high].iloc[0])
#     recent_o = lnear(data[low].iloc[0])
#     ohlc_list = data.to_dict('records')[1:]
#     s = datetime.now()
#     for this_ohlc in ohlc_list:
#         if mode == 'X':
#             print(f"{this_ohlc['date']} curr_high {curr_high}: n_blocks_below(curr_high): {n_blocks_below(curr_high)} "
#                   f"recent_x: {recent_x} hnear(this_ohlc[high]) : {hnear(this_ohlc[high])}")
#             # TODO: CHECK THIS and ELIF LOGIC
#             if hnear(this_ohlc[high]) > n_blocks_below(curr_high):
#                 if hnear(this_ohlc[high]) > recent_x:
#                     pf_df.loc[hnear(this_ohlc[high]), curr_col] = 'X'
#                     print(f"{curr_col} {this_ohlc['date']} : {hnear(this_ohlc[high])} : X : {this_ohlc[high]}")
#                     recent_x = hnear(this_ohlc[high])
#                 curr_high = max(curr_high, hnear(this_ohlc[high]))
#             elif (not hnear(this_ohlc[high]) > recent_x) and (this_ohlc[low] < n_blocks_below(curr_high)): # TODO
#                 print(f"{this_ohlc['date']} curr_low {curr_low}: n_blocks_above(curr_low): {n_blocks_above(curr_low)}")
#                 in_list = pf_df[pf_df[curr_col] == 'X'][curr_col].index
#                 pf_df.loc[in_list[0]:in_list[-1], curr_col] = 'X'
#                 print(f"{curr_col} {this_ohlc['date']}  : {in_list[0]} : {in_list[-1]} : X add: {this_ohlc[high]}")
#                 # print(pf_df[pf_df[curr_col] == 'X'])
#                 new_col = 'col' + str(int(curr_col.split('col')[1]) + 1)
#                 curr_col = new_col
#                 pf_df[curr_col] = ''
#                 mode = 'O'
#                 pf_df.loc[lnear(this_ohlc[low]), curr_col] = 'O'
#                 loc = np.where(blocks == recent_x)[0][0]
#                 pf_df.loc[blocks[loc - 1], curr_col] = 'O'
#                 pf_df.loc[blocks[loc - 2], curr_col] = 'O'
#                 print(f"{curr_col} {this_ohlc['date']}  : {lnear(this_ohlc[low])} : O new : {this_ohlc[low]}")
#                 print(f"{curr_col} {this_ohlc['date']}  : {blocks[loc - 1]} : O fill 1: {this_ohlc[low]}")
#                 print(f"{curr_col} {this_ohlc['date']} : {blocks[loc - 2]} : O fill 2: {this_ohlc[low]}")
#                 # recent_x = lnear(this_ohlc[low])
#                 recent_o = lnear(this_ohlc[low])
#                 curr_high = 0
#                 curr_low = 1000000
#         elif mode == 'O':
#             print(f"{this_ohlc['date']} curr_low {curr_low}: n_blocks_above(curr_low): {n_blocks_above(curr_low)} recent_o: {recent_o}")
#             # TODO: CHECK THIS and ELIF LOGIC
#             if lnear(this_ohlc[low]) < n_blocks_above(curr_low):
#                 if lnear(this_ohlc[low]) < recent_o:
#                     pf_df.loc[lnear(this_ohlc[low]), curr_col] = 'O'
#                     print(f"{curr_col} {this_ohlc['date']}  : {lnear(this_ohlc[low])} : O : {this_ohlc[low]}")
#                     recent_o = lnear(this_ohlc[low])
#                 curr_low = min(curr_low, lnear(this_ohlc[low]))
#             elif (not lnear(this_ohlc[low]) < recent_o) and this_ohlc[high] > n_blocks_above(curr_low):
#                 print(f"{this_ohlc['date']} curr_high {curr_high}: n_blocks_below(curr_high): {n_blocks_below(curr_high)}")
#                 in_list = pf_df[pf_df[curr_col] == 'O'][curr_col].index
#                 pf_df.loc[in_list[0]:in_list[-1], curr_col] = 'O'
#                 print(f"{curr_col} {this_ohlc['date']}  : {in_list[0]} : {in_list[-1]} : O add: {this_ohlc[low]}")
#                 new_col = 'col' + str(int(curr_col.split('col')[1]) + 1)
#                 curr_col = new_col
#                 pf_df[curr_col] = ''
#                 mode = 'X'
#                 pf_df.loc[hnear(this_ohlc[high]), curr_col] = 'X'
#                 loc = np.where(blocks == recent_o)[0][0]
#                 pf_df.loc[blocks[loc + 1], curr_col] = 'X'
#                 pf_df.loc[blocks[loc + 2], curr_col] = 'X'
#                 print(f"{curr_col} {this_ohlc['date']}  : {hnear(this_ohlc[high])} : X new : {this_ohlc[high]}")
#                 print(f"{curr_col} {this_ohlc['date']}  : {blocks[loc + 1]} : X fill 1: {this_ohlc[high]}")
#                 print(f"{curr_col} {this_ohlc['date']} : {blocks[loc + 2]} : X fill 2: {this_ohlc[high]}")
#                 recent_x = hnear(this_ohlc[high])
#                 # recent_o = lnear(this_ohlc[low])
#                 curr_high = 0
#                 curr_low = 1000000
#     in_list = pf_df[pf_df[curr_col] == mode][curr_col].index
#     pf_df.loc[in_list[0]:in_list[-1], curr_col] = mode
#
#     # for this_col in pf_df.columns:
#     #     pf_df.loc[pf_df[pf_df[this_col] != ''][this_col].index[-1], this_col] = ''
#
#     po_dict = get_po_new(pf_df)
#     po_dict['cmp_pf'] = data['close'].iloc[-1]
#     return pf_df, po_dict.copy()
#
#
#

def get_po_for_symbol(symbol, from_date='01/01/2020', first_time=True):
    data = ohlc_download.download_ohlc(symbol=symbol, from_date=from_date)
    data = data.dropna()
    close = 'adjclose'
    high = 'high'
    low = 'low'
    max_block = max(int(data['high'].max()) + 50, 300)
    blocks = np.concatenate((np.arange(0, 5, 0.25),
                             np.arange(5, 20, 0.5),
                             np.arange(20, 100, 1),
                             np.arange(100, 200, 2),
                             np.arange(200, max_block, 4)))

    def near(x):
        for i in range(0, len(blocks)):
            if blocks[i] <= x < blocks[i+1]:
                return blocks[i]

    def hnear(x):
        for i in range(0, len(blocks)):
            if blocks[i] <= x < blocks[i+1]:
                return blocks[i]

    def lnear(x):
        for i in range(0, len(blocks)):
            if blocks[i - 1] <= x < blocks[i]:
                return blocks[i]

    def n_blocks_below(price):
        if (price == 0) or (price == 1000000):
            return price
        loc = np.where(blocks == price)[0][0]
        return blocks[loc-PF_REVERSAL_POINTS]

    def n_blocks_above(price):
        if (price == 0) or (price == 1000000):
            return price
        loc = np.where(blocks == price)[0][0]
        return blocks[loc+PF_REVERSAL_POINTS]

    pf_df = pd.DataFrame(index=np.flip(blocks))
    pf_df['col1'] = ''
    curr_col = 'col1'
    mode = 'X'
    pf_df.loc[hnear(data[high].iloc[0]), 'col1'] = mode
    data['date'] = data.index
    curr_high = 0
    curr_low = 1000000
    recent_x = hnear(data[high].iloc[0])
    recent_o = lnear(data[low].iloc[0])
    ohlc_list = data.to_dict('records')[1:]
    s = datetime.now()
    for this_ohlc in ohlc_list:
        if mode == 'X':
            curr_high = max(curr_high, hnear(this_ohlc[high]))
            # print(f"{this_ohlc['date']} curr_high {curr_high}: n_blocks_below(curr_high): {n_blocks_below(curr_high)} "
            #       f"recent_x: {recent_x} hnear(this_ohlc[high]) : {hnear(this_ohlc[high])}")
            if hnear(this_ohlc[high]) > recent_x:
                pf_df.loc[hnear(this_ohlc[high]), curr_col] = 'X'
                # print(f"{curr_col} {this_ohlc['date']} : {hnear(this_ohlc[high])} : X : {this_ohlc[high]}")
                recent_x = hnear(this_ohlc[high])

            elif this_ohlc[low] < n_blocks_below(curr_high):
                # print(f"{this_ohlc['date']} curr_low {curr_low}: n_blocks_above(curr_low): {n_blocks_above(curr_low)}")
                in_list = pf_df[pf_df[curr_col] == 'X'][curr_col].index
                pf_df.loc[in_list[0]:in_list[-1], curr_col] = 'X'
                # print(f"{curr_col} {this_ohlc['date']}  : {in_list[0]} : {in_list[-1]} : X add: {this_ohlc[high]}")
                # print(pf_df[pf_df[curr_col] == 'X'])
                new_col = 'col' + str(int(curr_col.split('col')[1]) + 1)
                curr_col = new_col
                pf_df[curr_col] = ''
                mode = 'O'
                pf_df.loc[lnear(this_ohlc[low]), curr_col] = 'O'
                loc = np.where(blocks == recent_x)[0][0]
                pf_df.loc[blocks[loc - 1], curr_col] = 'O'
                pf_df.loc[blocks[loc - 2], curr_col] = 'O'
                # print(f"{curr_col} {this_ohlc['date']}  : {lnear(this_ohlc[low])} : O new : {this_ohlc[low]}")
                # print(f"{curr_col} {this_ohlc['date']}  : {blocks[loc - 1]} : O fill 1: {this_ohlc[low]}")
                # print(f"{curr_col} {this_ohlc['date']} : {blocks[loc - 2]} : O fill 2: {this_ohlc[low]}")
                # recent_x = lnear(this_ohlc[low])
                recent_o = lnear(this_ohlc[low])
                curr_high = 0
                curr_low = recent_o
        elif mode == 'O':
            curr_low = min(curr_low, lnear(this_ohlc[low]))
            # print(
            #     f"{this_ohlc['date']} curr_low {curr_low}: n_blocks_above(curr_low): {n_blocks_above(curr_low)} recent_o: {recent_o}")
            if lnear(this_ohlc[low]) < recent_o:
                pf_df.loc[lnear(this_ohlc[low]), curr_col] = 'O'
                # print(f"{curr_col} {this_ohlc['date']}  : {lnear(this_ohlc[low])} : O : {this_ohlc[low]}")
                recent_o = lnear(this_ohlc[low])

            elif this_ohlc[high] > n_blocks_above(curr_low):
                # print(f"{this_ohlc['date']} curr_high {curr_high}: n_blocks_below(curr_high): {n_blocks_below(curr_high)}")
                in_list = pf_df[pf_df[curr_col] == 'O'][curr_col].index
                pf_df.loc[in_list[0]:in_list[-1], curr_col] = 'O'
                # print(f"{curr_col} {this_ohlc['date']}  : {in_list[0]} : {in_list[-1]} : O add: {this_ohlc[low]}")
                new_col = 'col' + str(int(curr_col.split('col')[1]) + 1)
                curr_col = new_col
                pf_df[curr_col] = ''
                mode = 'X'
                pf_df.loc[hnear(this_ohlc[high]), curr_col] = 'X'
                loc = np.where(blocks == recent_o)[0][0]
                pf_df.loc[blocks[loc + 1], curr_col] = 'X'
                pf_df.loc[blocks[loc + 2], curr_col] = 'X'
                # print(f"{curr_col} {this_ohlc['date']}  : {hnear(this_ohlc[high])} : X new : {this_ohlc[high]}")
                # print(f"{curr_col} {this_ohlc['date']}  : {blocks[loc + 1]} : X fill 1: {this_ohlc[high]}")
                # print(f"{curr_col} {this_ohlc['date']} : {blocks[loc + 2]} : X fill 2: {this_ohlc[high]}")
                recent_x = hnear(this_ohlc[high])
                # recent_o = lnear(this_ohlc[low])
                curr_high = recent_x
                curr_low = 1000000
    in_list = pf_df[pf_df[curr_col] == mode][curr_col].index
    pf_df.loc[in_list[0]:in_list[-1], curr_col] = mode
    if first_time and len(pf_df.columns) < 10:
        return get_po_for_symbol(symbol=symbol, from_date='01/01/2018', first_time=False)
    # for this_col in pf_df.columns:
    #     pf_df.loc[pf_df[pf_df[this_col] != ''][this_col].index[-1], this_col] = ''

    po_dict = get_po_new(pf_df)
    po_dict['cmp_pf'] = data['close'].iloc[-1]
    return pf_df, po_dict.copy()
