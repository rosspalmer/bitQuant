import numpy as np
from pandas import DataFrame
from pandas.tseries.tools import to_datetime
from time import mktime
from datetime import datetime

#|Convert trades data to price data
def olhcv(trd, freq, exchange='', symbol='', tsmp_col='no'):

	price = trd['price'].astype(float)	
	amount = trd['amount'].astype(float)
	priceamprod = price * amount	
	prc = DataFrame(index=price.resample(freq, how='last').index)	
	
	#|Use pandas 'resample' function to create OLHCV data
	prc['open'] = price.resample(freq, how='first').fillna(value=0)
	prc['low'] = price.resample(freq, how='min').fillna(value=0)
	prc['high'] = price.resample(freq, how='max').fillna(value=0)
	prc['close'] = price.resample(freq, how='last').fillna(method='ffill')
	prc['volume'] = amount.resample(freq, how='sum').fillna(value=0)
	# avoiding zeros in volume for VWAP
	vwap = priceamprod.resample(freq, how='sum') / amount.resample(freq, how='sum')
	prc['vwap'] = vwap.fillna(value=0)
	prc = prc.apply(replace_zero, axis=1)	

	#|Add exchange, source, and freq columns if required
	prc['freq'] = freq	
	if exchange <> '':
		prc['exchange'] = exchange
	elif 'exchange' in trd:	
		prc['exchange'] = trd['exchange'].iloc[0]
	if symbol <> '':
		prc['symbol'] = symbol
	elif 'symbol' in trd:
		prc['symbol'] = trd['symbol'].iloc[0]

	#|Add timestamp column if required
	if tsmp_col == 'yes':
		prc['timestamp'] = prc.index.astype(np.int64) // 10**9

	#|Slice price data to cut off incomplete ends
	prc = prc[1:-1]
	return prc

#|Replace zeros in open, low, and high with the last close
def replace_zero(row):
	if row['open'] == 0:
		row['open'] = row['close']
		row['low'] = row['close']
		row['high'] = row['close']
		return row
	else:
		return row

#|Create datetime index for DataFrame using "timestamp" column
def date_index(df):
	date = df['timestamp']
	date = to_datetime(date, unit='s')
	df['date'] = date
	df = df.set_index('date')
	return df

#|Convert datetime sting (format: mm/dd/yy) to timestamp
def dateconv(date):
	try:
		date = datetime.strptime(date, "%m/%d/%y")
	except:
		date = datetime.strptime(date, "%Y-%m-%d")		
	timestamp = int(mktime(date.timetuple()))		
	return timestamp

#|Convert column names in DataFrame to 'standard'
#|column names and return DataFrame	
def standard_columns(df):
	cols = []	
	headers = {'tid':'tid','trade_id':'tid',
		'price':'price',
		'amount':'amount','size':'amount',
		'type':'type','side':'type',		
		'timestamp':'timestamp','date':'timestamp',
		'timestamp_ms':'timestamp_ms','date_ms':'timestamp_ms',
		'exchange':'exchange',
		'Open':'open',
		'Low':'low',
		'High':'high',
		'Close':'close',
		'Volume (BTC)':'volume',
		'Weighted Price':'vwap',
		'source':'source',
		'freq':'freq'}
	for col in df:
		if col in headers.keys():
			cols.append(headers[col])
		else:
			df = df.drop(col, axis=1)
	df.columns = cols
	return df

