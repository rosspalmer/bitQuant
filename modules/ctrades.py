import db

from time import mktime
from datetime import datetime
from pandas import DataFrame

class trades(object):
	
	def __init__(self):
		self.df = DataFrame(columns=('tid','price','amount','type', 'exchange',
					'timestamp','timestamp_ms','dbtable'))
		self.ts = DataFrame(columns=('timestamp','price','high',
					'low','open','amount'))

	def add(self, table_name, exchange='', start='', end=''):
		df = db.trades_df(table_name, exchange=exchange,
				start=start, end=end)
		df = db.date_index(df)
		df['dbtable'] = table_name
		self.df = self.df.append(df)
		self.df = self.df.sort()

	def time_series(self, period):
		tmin = int(self.df['timestamp'].min())
		tmax = int(self.df['timestamp'].max())
		for tsmp in range(tmin, tmax, period):
			df, slic = time_slice(self.df, tsmp, period)		
			self.ts = self.ts.append(slic)
		self.ts = db.date_index(self.ts)

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
	return df, slic



		
