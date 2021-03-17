
import datetime
s = datetime.datetime.now()
a = get_options_filter(['AAPL'])
print(datetime.datetime.now()-s)

from ib_insync import *

ib = IB()
ib.connect("127.0.0.1", 7497, clientId=10)


spx = Index('SPX', 'CBOE')
ib.qualifyContracts(spx)

