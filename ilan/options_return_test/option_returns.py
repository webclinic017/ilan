import pandas as pd
import numpy as np
from yahoo_finance_api import option_chains_provider
from config import *


def get_options_filter(symbols_list):
    options_df = option_chains_provider.get_data_for_symbols(symbols_list)
    options_df['current_date'] = pd.to_datetime(datetime.today().date())
    options_df['days_in_trade'] = (options_df['option_expiry_date'] - options_df['current_date']).dt.days + 1
    options_df['lot_size'] = 100
    options_df['deal_roi'] = np.where(options_df['stock_price'] > options_df['option_strike_price'],
                                      (options_df['option_premium'] - BUY_COMMISSION
                                       - (options_df['stock_price'] - options_df['option_strike_price'])) / options_df['stock_price'],
                                      (options_df['option_premium'] - BUY_COMMISSION) / (options_df['stock_price']))
    options_df['day_roi'] = options_df['deal_roi'] / options_df['days_in_trade']
    options_df['annual_roi'] = options_df['day_roi'] * 252
    options_df['is_far_strike'] = np.where(abs((options_df['option_strike_price']
                                                - options_df['stock_price'])/options_df['stock_price']) > 0.5, 1, 0)
    options_df['is_zero_bid'] = np.where(options_df['option_bid'] == 0, 1, 0)
    options_df['is_zero_ask'] = np.where(options_df['option_ask'] == 0, 1, 0)
    options_df['options_result'] = np.where((options_df['annual_roi'] >= OPTIONS_PASS_CRITERIA) &
                                            (options_df['option_volume'] >= MIN_VOLUME) &
                                            (options_df['option_oi'] >= MIN_OI) &
                                            (options_df['is_far_strike'] == 0) &
                                            (options_df['is_zero_bid'] == 0) &
                                            (options_df['is_zero_ask'] == 0), 'PASS', 'FAIL')
    # options_df.to_csv('all_symbols_option_test_15_feb.csv')
    return options_df[['last_update_utc_time', 'stock_symbol', 'stock_price', 'option_symbol', 'option_type',
                       'option_strike_price', 'option_premium', 'option_recent_trade_date', 'option_bid', 'option_ask',
                       'option_change', 'option_change_pct',  'option_implied_volatility',  'option_expiry_date',
                       'option_volume', 'option_oi', 'current_date', 'days_in_trade', 'lot_size', 'deal_roi', 'day_roi',
                       'annual_roi', 'is_far_strike', 'is_zero_bid', 'is_zero_ask', 'options_result']]

