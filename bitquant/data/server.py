import db

import pandas as pd

#|Update price data using recent API trade data
def ttop_update(exchange='',freq=''):
	prc = db.price_df(freq=freq, exchange=exchange, source='api')
	last = last_timestamp(prc)
	trd = db.trades_df('api', exchange=exchange, start=last)
	for exchange in prc['exchange'].unique():
		for freq in prc['freq'].unique():
			trd = trd[trd['exchange'] == exchange]
			db.trades_to_pricedb(trd, freq, 'api')
			
#|Determine second to last timestamp for all exchange-freq combinations		
def last_timestamp(prc):
	last = []
	for exchange in prc['exchange'].unique():
		eprc = prc[prc['exchange'] == exchange]		
		for freq in prc['freq'].unique():
			fprc = eprc[eprc['freq'] == freq]		
			tlast = [fprc['timestamp'].iloc[-2]]
			last = last + tlast
	last = int(min(last))
	return last
	 

