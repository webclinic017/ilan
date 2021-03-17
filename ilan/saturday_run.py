"""
Run this file every saturday US evening 5 PM (UTC 22:00 HRS)
see WEEKEND_RUN_TIME_UTC in config.py
"""
from email_alerts import email_sender
from files_and_paths import *
from config import *
from main import update_symbols


if __name__ == '__main__':
    update_symbols()
    today_str = str(datetime.utcnow().date()).replace('-', '_')
    email_sender.send_mail(send_from='djhfortrade@gmail.com',
                           send_to=EMAIL_LIST, subject=f'DJH | {today_str} | Automated Email | Symbols for upcoming week',
                           message=f'PFA Symbols list for upcoming week',
                           files=[symbols_file])
    print(f"Email sent to {EMAIL_LIST}")
