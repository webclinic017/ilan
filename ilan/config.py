from datetime import datetime, time, timedelta

N_RECENT_DAYS = 60
MIN_VOLUME = 0
MIN_OI = 1
BUY_COMMISSION = 0.0065
STOCK_SCREEN_VOLUME = 25000
# Pass criteria

OPTIONS_PASS_CRITERIA = 0.3
ANALYST_PASS_CRITERIA = 0.75
PE_PASS_CRITERIA = 17
PF_PASS_CRITERIA = 0.30

PF_REVERSAL_POINTS = 3

EMAIL_LIST = ['sriramkjs@gmail.com', 'ilanhzm@gmail.com']

# MARKET HOURS AND RUN TIMES
MARKET_OPEN_UTC = time(14, 30)
MARKET_CLOSE_UTC = time(21, 00)
EOD_RUN_TIME_UTC = time(22, 00)
WEEKEND_RUN_TIME_UTC = time(22, 00)