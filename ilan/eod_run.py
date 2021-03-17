"""
Run this fill every weekday US time 5 PM (22:00 UTC) (Monday to Friday)
see EOD_RUN_TIME_UTC in config.py
"""

from main import eod_stock_filter, options_test
import os
from files_and_paths import *
from config import *
from email_alerts import email_sender

if __name__ == '__main__':
    eod_stock_filter()
    options_test()
    recent_date = max(os.listdir(reports_folder))
    file_list = [str(reports_folder) + str(i) for i in os.listdir(reports_folder+recent_date)]
    email_sender.send_mail(send_from='djhfortrade@gmail.com',
                           send_to=EMAIL_LIST, subject=f'DJH | {recent_date} | Automated Email | EOD Stock filter',
                           message=f'PFA Screener excel for DJH for {recent_date}',
                           files=[symbols_file])
    print(f"Email sent to {EMAIL_LIST}")

