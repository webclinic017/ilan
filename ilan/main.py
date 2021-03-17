"""
Weekly update: Symbols list
Daily EOD: Step 2, 3, 4
Daily EOD: Step 1 on filtered stocks of 2, 3, 4
Intraday: Step 1 on filtered stocks of 2, 3, 4
1. List of symbols
2. Options filter
3. P&F filter
4. Market watch filter
"""

import os
import numpy as np
from yahoo_fin.stock_info import *
from files_and_paths import *
from datetime import datetime
from config import *
from options_return_test import option_returns
from momentum_test import price_objective
from analyst_recco_test import analyst_estimates
from fundamentals_test import fundamentals
from email_alerts import email_sender
from yahoo_finance_api import symbols_manager


def update_symbols():
    symbols_manager.download_symbols_list()


def eod_stock_filter():
    today_str = str(datetime.now().date()).replace('-', '_')
    if not os.path.isdir(reports_folder + today_str):
        os.mkdir(reports_folder + today_str)

    s = datetime.now()
    symbols_list = symbols_manager.get_symbols_list()
    pf_df_dict, po_df = price_objective.get_po_for_symbols(symbols_list=symbols_list)
    fundamental_df = fundamentals.get_fundamentals(symbols_list=symbols_list)
    analyst_df = analyst_estimates.get_analyst_estimates(symbols_list=symbols_list)

    stock_results_df = fundamental_df[['ticker', 'fundamentals_pe_result']].merge(po_df[['ticker', 'pf_result']], on='ticker',
                                                                            how='outer')
    stock_results_df = stock_results_df.merge(analyst_df[['ticker', 'analyst_result']], on='ticker', how='outer')
    stock_results_df['STOCK_RESULT'] = np.where((stock_results_df['fundamentals_pe_result'] == 'PASS') &
                                            (stock_results_df['pf_result'] == 'PASS') &
                                            (stock_results_df['analyst_result'] == 'PASS'), 'PASS', 'FAIL')
    stock_filter_file_name = 'stock_filter_{}.xlsx'.format(today_str)
    writer = pd.ExcelWriter(reports_folder + today_str + '/' + stock_filter_file_name, engine='xlsxwriter')
    stock_results_df.to_excel(writer, sheet_name='STOCK FILTER RESULT', index=False)
    po_df.to_excel(writer, sheet_name='Momentum', index=False)
    analyst_df.to_excel(writer, sheet_name='Analyst Estimates', index=False)
    fundamental_df.to_excel(writer, sheet_name='Fundamentals', index=False)
    writer.save()
    writer.close()

    # write_pf_charts(pf_df_dict=pf_df_dict, today_str=today_str)

    print(datetime.now()-s)


def options_test():
    recent_date = max(os.listdir(reports_folder))
    filter_df = pd.read_excel(f'{reports_folder}/{recent_date}/stock_filter_{recent_date}.xlsx', sheet_name='STOCK FILTER RESULT')
    pass_df = filter_df[filter_df['STOCK_RESULT'] == 'PASS']
    if len(pass_df) > 0:
        pass_symbols_list = pass_df['ticker'].to_list()
        options_df = option_returns.get_options_filter(symbols_list=pass_symbols_list)
        if len(options_df) > 0:
            option_pass_df = options_df[options_df['options_result'] == 'PASS']
            all_options_files = [i for i in os.listdir(reports_folder+recent_date) if 'options_' in i]
            if len(all_options_files) == 0:
                option_filter_file_name = 'options_test_{}.xlsx'.format(recent_date)
            else:
                suffix = str(datetime.utcnow()).replace('-', '_').replace(' ', '_').replace(':', '_').split('.')[0]
                option_filter_file_name = 'options_test_{}.xlsx'.format(suffix)
            writer = pd.ExcelWriter(reports_folder + recent_date + '/' + option_filter_file_name, engine='xlsxwriter')
            option_pass_df.to_excel(writer, sheet_name='OPTIONS TEST RESULT', index=False)
            options_df.to_excel(writer, sheet_name='Options test', index=False)
            writer.save()
            writer.close()


# Write charts
def write_pf_charts(pf_df_dict, today_str):
    pf_file_name = 'pf_{}.xlsx'.format(today_str)
    writer = pd.ExcelWriter(reports_folder + today_str + '/' + pf_file_name, engine='xlsxwriter')
    for this_key in pf_df_dict:
        df = pf_df_dict[this_key]
        df.to_excel(writer, sheet_name=this_key, index=True)
    writer.save()
    writer.close()


def email_files(files_list, today_str):
    # files_list = [reports_folder + today_str + '/' + filter_file_name, reports_folder + today_str + '/' + pf_file_name]
    email_sender.send_mail(send_from='djhfortrade@gmail.com',
                           send_to=EMAIL_LIST, subject=f'DJH | {today_str} | Automated Email',
                           message=f'PFA Screener excel for DJH for {today_str}',
                           files=files_list)
    print(f"Email sent to {EMAIL_LIST}")
