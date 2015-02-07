import sql

import pandas as pd
import time as tm

#|Update price data using recent API trade data
def ttop_update(exchange='',freq=''):
	prc = sql.price_df(freq=freq, exchange=exchange, source='api')
	last = last_timestamp(prc)
	trd = sql.trades_df('api', exchange=exchange, start=last)
	for exchange in prc['exchange'].unique():
		for freq in prc['freq'].unique():
			trd = trd[trd['exchange'] == exchange]
			print trd
			sql.trades_to_pricedb(trd, freq, 'api')
			
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

#|Function used for cron job scripts	 
def cron_run(interval=3600, rate=30):
	start = tm.time()	
	exchanges = ['bitfinex','btcchina']
	last = tm.time()-rate
	while int(tm.time()-start) < interval:
		if int(tm.time()-last) > rate-1:
			last = tm.time()			
			for exchange in exchanges:
				api_ping(exchange, limit=500)			
			if tm.time()-last < rate-3:
				tm.sleep(int(rate-(tm.time() - last)-3))

#|"Ping" exchange API for trade data and import into SQL database
def api_ping(exchange, limit=100):
	db = sql.dbconnect()
	trd = api.trades(exchange, limit)	
	db.df_to_sql(trd, 'api')
	
#|Convert trade history to price and add to SQL database
def trades_to_pricedb(trd, freq, source):
	db = sql.dbconnect()
	prc = tools.trades_to_price(trd, freq, source=source)
	prc['timestamp'] = prc.index.astype(np.int64) // 10**9
	prc['freq'] = freq
	db.df_to_sql(prc, 'price')
	
		
	
