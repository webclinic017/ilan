"""
Run this between US market opening (9 30 AM) and close (4 PM) on all weekdays
see MARKET_OPEN_UTC and MARKET_CLOSE_UTC in config.py
"""

from main import eod_stock_filter, options_test
import os
from files_and_paths import *
from config import *
from email_alerts import email_sender
from time import sleep


if __name__ == '__main__':
    start_time_utc = time(14, 30)
    end_time_utc = time(21, 00)
    while True:
        if datetime.utcnow().time() > start_time_utc and datetime.utcnow().time() < end_time_utc:
            options_test()
            recent_date = max(os.listdir(reports_folder))
            file_list = [str(reports_folder) + str(i) for i in os.listdir(reports_folder+recent_date)]
            email_sender.send_mail(send_from='djhfortrade@gmail.com',
                                   send_to=EMAIL_LIST, subject=f'DJH | {recent_date} | Automated Email | Intraday options filter',
                                   message=f'PFA Intraday options screener excel for DJH for {recent_date} @ UTC {datetime.utcnow()}',
                                   files=[symbols_file])
            print(f"Email sent to {EMAIL_LIST}")
            # Sleep for 20 minutes before next run
            sleep(20 * 60)
        else:
            print("Completed intraday run for the day")
            break
