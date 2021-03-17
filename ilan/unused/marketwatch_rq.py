import requests
from bs4 import BeautifulSoup

url = 'https://www.marketwatch.com/investing/stock/amzn/analystestimates?mod=mw_quote_tab'
r =  requests.get(url=url)
html_soup = BeautifulSoup(r.text, 'html.parser')
data_response = html_soup.find_all('div',attrs={'class':'bar-chart'})

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

data = {'3m_buy':Buy_3M_AGO, '3m_overweight': Overweight_3M_AGO, '3m_hold':Hold_3M_AGO, '3m_underweight': Underweight_3M_AGO, '3m_sell': Sell_3M_AGO,
'1m_buy':Buy_1M_AGO, '1m_overweight': Overweight_1M_AGO, '1m_hold':Hold_1M_AGO, '1m_underweight': Underweight_1M_AGO, '1m_sell': Sell_1M_AGO,
'curr_buy':Buy_CURRENT, 'curr_overweight': Overweight_CURRENT, 'curr_hold':Hold_CURRENT, 'curr_underweight': Underweight_CURRENT, 'curr_sell': Sell_CURRENT }

print(data)
