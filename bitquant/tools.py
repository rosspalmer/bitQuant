from pandas import DataFrame
from pandas.tseries.tools import to_datetime
from time import mktime
from datetime import datetime

#|Convert trades DF to price DF
def trades_to_price(trd, freq, source=''):
	
	price = trd['price']	
	amount = trd['amount']	
	prc = DataFrame(index=price.resample(freq, how='last').index)	
	
	prc['price'] = price.resample(freq, how='last').fillna(method='ffill')
	prc['open'] = price.resample(freq, how='first').fillna(value=0)
	prc['high'] = price.resample(freq, how='max').fillna(value=0)
	prc['low'] = price.resample(freq, how='min').fillna(value=0)
	
	prc['amount'] = amount.resample(freq, how='sum').fillna(value=0)
	prc['exchange'] = trd['exchange'].iloc[0]	
	if source <> '':
		prc['source'] = source
	prc = prc[1:-1]
	return prc

#|Create datetime index for DataFrame using "timestamp" column
def date_index(df):
	date = df['timestamp']
	date = to_datetime(date, unit='s')
	df['date'] = date
	df = df.set_index('date')
	return df

#|Convert datetime sting (format: mm/dd/yy) to timestamp
def dateconv(date):	
	date = datetime.strptime(date, "%m/%d/%y")		
	timestamp = int(mktime(date.timetuple()))		
	return timestamp
	
