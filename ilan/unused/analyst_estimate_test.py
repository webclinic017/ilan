"""
'https://www.marketwatch.com/investing/stock/amzn/analystestimates?mod=mw_quote_tab'
"""

from yahoo_fin.stock_info import *
import datetime
from unused import scrap_marketwatch

url = 'https://www.marketwatch.com/investing/stock/{}/analystestimates?mod=mw_quote_tab'
symbols_list = tickers_dow()
estimates_list = list()
for this_symbol in symbols_list:
    s = datetime.datetime.now()
    print(f"Scraping marketwatch.com for {this_symbol}")
    symbol_url = url.format(this_symbol.lower())
    try:
        s_dict = scrap_marketwatch.scrap_analyst_estimates(symbol_url)
        s_dict['symbol'] = this_symbol
        s_dict['update_datetime_utc'] = datetime.datetime.utcnow()
        estimates_list.append(s_dict.copy())
    except:
        print(f"Scraping failed in marketwatch.com for {this_symbol}")
    print(datetime.datetime.now() - s)

estimate_df = pd.DataFrame(estimates_list)
estimate_df.to_csv('analyst_estimates.csv')
