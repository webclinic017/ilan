import pandas as pd
from selenium import webdriver
from time import sleep
from datetime import datetime


def scrap_analyst_estimates(url):
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    # driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    driver.get(url)

    Buy_3M_AGO = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > span').text
    Buy_1M_AGO = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(1) > td:nth-child(3) > div > span').text
    Buy_CURRENT = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(1) > td:nth-child(4) > div > span').text

    Overweight_3M_AGO = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > span').text
    Overweight_1M_AGO = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > span').text
    Overweight_CURRENT = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(2) > td:nth-child(4) > div > span').text

    Hold_3M_AGO = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(3) > td:nth-child(2) > div > span').text
    Hold_1M_AGO = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(3) > td:nth-child(3) > div > span').text
    Hold_CURRENT = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(3) > td:nth-child(4) > div > span').text

    Underweight_3M_AGO = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(4) > td:nth-child(2) > div > span').text
    Underweight_1M_AGO = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(4) > td:nth-child(3) > div > span').text
    Underweight_CURRENT = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(4) > td:nth-child(4) > div > span').text

    Sell_3M_AGO = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(5) > td:nth-child(2) > div > span').text
    Sell_1M_AGO = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(5) > td:nth-child(3) > div > span').text
    Sell_CURRENT = driver.find_element_by_css_selector('body > div.container.container--body > div.region.region--primary > div.column.column--primary > div.element.element--analyst.analyst-ratings > table > tbody > tr:nth-child(5) > td:nth-child(4) > div > span').text

    # data = {
    #     '3M_AGO':[Buy_3M_AGO, Overweight_3M_AGO, Hold_3M_AGO, Underweight_3M_AGO, Sell_3M_AGO],
    #     '1M_AGO':[Buy_1M_AGO, Overweight_1M_AGO, Hold_1M_AGO, Underweight_1M_AGO, Sell_1M_AGO],
    #     'CURRENT':[Buy_CURRENT, Overweight_CURRENT, Hold_CURRENT, Underweight_CURRENT, Sell_CURRENT]
    # }

    # df = pd.DataFrame(data, index=['Buy', 'Overweight', 'Hold', 'Underweight', 'Sell'])

    # print(df)
    # now = datetime.now()
    # dt_string = now.strftime("%d_%m_%Y %Hh%Mm%Ss")
    # df.to_csv(dt_string +'.csv', index=True, encoding='utf-8')

    data = {'3m_buy':Buy_3M_AGO, '3m_overweight': Overweight_3M_AGO, '3m_hold':Hold_3M_AGO, '3m_underweight': Underweight_3M_AGO, '3m_sell': Sell_3M_AGO,
    '1m_buy':Buy_1M_AGO, '1m_overweight': Overweight_1M_AGO, '1m_hold':Hold_1M_AGO, '1m_underweight': Underweight_1M_AGO, '1m_sell': Sell_1M_AGO,
    'curr_buy':Buy_CURRENT, 'curr_overweight': Overweight_CURRENT, 'curr_hold':Hold_CURRENT, 'curr_underweight': Underweight_CURRENT, 'curr_sell': Sell_CURRENT }

    return data.copy()
