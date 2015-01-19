from pandas import DataFrame
from pandas.tseries.tools import to_datetime

#|Create time series from trade history DataFrame
def time_series(df, period):
	ts = DataFrame(columns=('timestamp', 'price', 'high',
				'low', 'open', 'amount'))	
	tmin = int(df['timestamp'].min())
	tmax = int(df['timestamp'].max())
	for tsmp in range(tmin, tmax, period):
		slic = time_slice(df, tsmp, period)		
		ts = ts.append(slic)
	ts = date_index(ts)
	return ts

def time_slice(df, tsmp, period):
	lprice = df[df['timestamp'] < tsmp].tail(1)['price']
	df = df[df['timestamp'] >= tsmp]
	df = df[df['timestamp'] < (tsmp + period)]	
	if len(df.index) == 0:
		slic = DataFrame({'timestamp' : [tsmp], 'price': lprice, 
				'high': lprice, 'low': lprice,
				'open': lprice, 'amount': 0.0})		
	else:			
		slic = DataFrame({'timestamp' : [tsmp], 
				'price': round(df['price'].iloc[-1], 3),
				'high': round(df['price'].max(), 3), 
				'low': round(df['price'].min(), 3),
				'open': round(df['price'].iloc[0], 3), 
				'amount': round(df['amount'].sum(), 4)})		
	return slic

#|Create datetime index for DataFrame using "timestamp" column
def date_index(df):
	date = df['timestamp']
	date = to_datetime(date, unit='s')
	df['date'] = date
	df = df.set_index('date')
	return df

#Outputs number of seconds in provided number of days/hours/minutes
def seconds(days=0, hours=0, minutes=0, typ=''):
	if typ == '':	
		total = 86400*days + 3600*hours + 60*minutes
	elif typ == 'd':
		total = 86400
	elif typ == 'h':
		total = 3600
	elif typ == 'm':
		total = 50
	return total


