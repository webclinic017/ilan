import pandas as pd
import requests
import os
import sys

from bs4 import BeautifulSoup
from datetime import date, timedelta, datetime

from pandas import json_normalize
from pprint import pprint as pp
from requests import get
from requests.packages import urllib3
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from tqdm import tqdm
from warnings import warn
from config import *
from files_and_paths import *


def get_data_for_country(country='United States', save_path=symbols_file, avg_vol=STOCK_SCREEN_VOLUME):
    raw_data = {
        'Symbol':[],
        'Name': [],
        'Price_Intraday':[],
        'Change': [],
        '%Change': [],
        'Volume':[],
        'Avg_Vol':[],
        'Market_Cap':[],
        'PE_Ratio':[]
    }

    # activates widnow with below link
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    # driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://finance.yahoo.com/screener/new')
    sleep(1)

    # remove US selection
    us_slection_xpath = '//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li[1]'
    driver.find_element_by_xpath(us_slection_xpath).click()
    sleep(1)

    # click on Add region button
    add_region_xpath = '//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li'
    driver.find_element_by_xpath(add_region_xpath).click()
    sleep(1)

    # selecting
    driver.find_element_by_xpath(
        "//div[@id='dropdown-menu']//input[@class='Bd(0) H(28px) Bgc($lv3BgColor) C($primaryColor) W(100%) Fz(s) Pstart(28px)']").send_keys(
        country)
    sleep(5)
    driver.find_element_by_xpath(
        "//div[@id='dropdown-menu']//span[@class='C($tertiaryColor) Mstart(12px) Cur(p) Va(m)']").click()
    # selecting Canada button
    sleep(5)
    # Filter volume
    driver.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[6]/button/span/span').click()
    driver.find_element_by_css_selector(
        '#screener-criteria > div.Pos\(r\).Pt\(16px\).Pb\(20px\).Bd.Bdc\(\$seperatorColor\).W\(100\%\).Bgc\(\$headerBgColor\).Bdrs\(3px\) > div.Mstart\(22px\).Pend\(25px\).Mstart\(10px\)--mobp.Pend\(10px\)--mobp.Mstart\(10px\)--mobl.Pend\(10px\)--mobl > div.D\(ib\).Fl\(start\).Mt\(10px\) > div.Pos\(r\).Mt\(8px\).Mb\(15px\) > div > div > div.Pstart\(25px\).Pend\(20px\).Mah\(400px\).Mah\(550px\)--tab768.Mah\(315px\)--mobp.Mah\(315px\)--mobl.Ovy\(a\) > div:nth-child(1) > div > ul > li:nth-child(2) > label > svg').click()
    sleep(2)
    driver.find_element_by_css_selector(
        '#screener-criteria > div.Pos\(r\).Pt\(16px\).Pb\(20px\).Bd.Bdc\(\$seperatorColor\).W\(100\%\).Bgc\(\$headerBgColor\).Bdrs\(3px\) > div.Mstart\(22px\).Pend\(25px\).Mstart\(10px\)--mobp.Pend\(10px\)--mobp.Mstart\(10px\)--mobl.Pend\(10px\)--mobl > div.D\(ib\).Fl\(start\).Mt\(10px\) > div.Pos\(r\).Mt\(8px\).Mb\(15px\) > div > div > button > svg > path').click()
    sleep(2)
    # input value greater than
    driver.find_element_by_xpath(
        "//div[@class='Mstart(22px) Pend(25px) Mstart(10px)--mobp Pend(10px)--mobp Mstart(10px)--mobl Pend(10px)--mobl']/div[@class='D(ib) Fl(start) Mt(10px)']/div[@class='Mb(5px) C($tertiaryColor)'][6]/div[@class='D(ib) Bgc($lv2BgColor) Bdrs(3px) Py(12px) Pstart(18px) Pend(20px) Px(10px)--mobp Px(10px)--mobl W(85%)--mobp W(92%)--mobl Px(10px)--tab768']/div[@class='D(ib) W(100%)--mobp W(100%)--mobl W(560px)--scrm W(510px)--scrl W(428px)!--tab768']/input[@class='Fz(s) Pstart(8px) H(28px) Bgc($lv3BgColor) C($primaryColor) W(110px) Bdc($seperatorColor) Bdc($linkColor):f']").send_keys(
        avg_vol)
    sleep(5)

    # click on search
    find_button_xpath = '//*[@id="screener-criteria"]/div[2]/div[1]/div[3]/button[1]'
    driver.find_element_by_xpath(find_button_xpath).click()
    sleep(5)
    Estimated_results = driver.find_element_by_xpath("//div[@class='Fw(b) Fz(36px)']").text
    Estimated_results = int(Estimated_results)

    print("Estimated_results = ", Estimated_results)

    # getting current url
    url = driver.current_url

    # creating an empty list for code
    # loop through code using bs4

    for i in tqdm(range(0, Estimated_results, 25), position = 0):

        new_url = str(url) + '?count=25&offset=' + str(i)
        sleep(3)
        response = get(new_url)
        sleep(3)
        html_soup = BeautifulSoup(response.text, 'html.parser')

        list_all_cd = html_soup.findAll('tr', attrs={
            'class': 'simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv2BgColor)'})
        j = 0
        for cd in list_all_cd:
            companies = cd.find('a', {"class": "Fw(600) C($linkColor)"}).text
            # print(companies)
            name1 = cd.find('td', {"class": "Va(m) Ta(start) Px(10px) Fz(s)"}).text
            # print(name1)
            Price_Intraday = cd.find('td', {"class": "Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)"}).text
            Change = cd.find('td', {"aria-label": "Change"}).text
            Change1 = cd.find('td', {"aria-label": "% Change"}).text
            Volume = cd.find('td', {"aria-label": "Volume"}).text
            Avg_Vol = cd.find('td', {"aria-label": "Avg Vol (3 month)"}).text
            Market_Cap = cd.find('td', {"class": "Va(m) Ta(end) Pstart(20px) Pend(10px) W(120px) Fz(s)"}).text
            PE_Ratio = cd.find('td', {"aria-label": "PE Ratio (TTM)"}).text
            raw_data['Symbol'].append(companies)
            raw_data['Name'].append(name1)
            raw_data['Price_Intraday'].append(Price_Intraday)
            raw_data['Change'].append(Change)
            raw_data['%Change'].append(Change1)
            raw_data['Volume'].append(Volume)
            raw_data['Avg_Vol'].append(Avg_Vol)
            raw_data['Market_Cap'].append(Market_Cap)
            raw_data['PE_Ratio'].append(PE_Ratio)

            j = j + 1

        # get data is missed

        list_all_cd2 = html_soup.findAll('tr', attrs={
            'class': 'simpTblRow Bgc($hoverBgColor):h BdB Bdbc($seperatorColor) Bdbc($tableBorderBlue):h H(32px) Bgc($lv1BgColor)'})
        j = 0
        for cd in list_all_cd2:
            companies = cd.find('a', {"class": "Fw(600) C($linkColor)"}).text
            # print(companies)
            name1 = cd.find('td', {"class": "Va(m) Ta(start) Px(10px) Fz(s)"}).text
            # print(name1)
            Price_Intraday = cd.find('td', {"class": "Va(m) Ta(end) Pstart(20px) Fw(600) Fz(s)"}).text
            Change = cd.find('td', {"aria-label": "Change"}).text
            Change1 = cd.find('td', {"aria-label": "% Change"}).text
            Volume = cd.find('td', {"aria-label": "Volume"}).text
            Avg_Vol = cd.find('td', {"aria-label": "Avg Vol (3 month)"}).text
            Market_Cap = cd.find('td', {"class": "Va(m) Ta(end) Pstart(20px) Pend(10px) W(120px) Fz(s)"}).text
            PE_Ratio = cd.find('td', {"aria-label": "PE Ratio (TTM)"}).text
            raw_data['Symbol'].append(companies)
            raw_data['Name'].append(name1)
            raw_data['Price_Intraday'].append(Price_Intraday)
            raw_data['Change'].append(Change)
            raw_data['%Change'].append(Change1)
            raw_data['Volume'].append(Volume)
            raw_data['Avg_Vol'].append(Avg_Vol)
            raw_data['Market_Cap'].append(Market_Cap)
            raw_data['PE_Ratio'].append(PE_Ratio)

            j = j + 1

        table = pd.DataFrame(raw_data, columns=['Symbol', 'Name', 'Price_Intraday', 'Change', '%Change', 'Volume',
                                                'Avg_Vol', 'Market_Cap', 'PE_Ratio'])
        f_name = symbols_file
        table.to_csv(f_name, index=False)
