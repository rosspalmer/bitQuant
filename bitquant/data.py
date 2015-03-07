import api
import sql
import tools

import datetime
from pandas import DataFrame

#|Used to convert trade history in MySQL database to price (OLHCV) data
class trades_to_price(object):
	
	#|Set variables and convert trade data to price data
	def __init__(self, exchange, symbol, freq, start=0, name=''):
		self.exchange = exchange
		self.symbol = symbol
		self.freq = freq
		self.start = start
		self.name = name
		self.prc = self.convert()

	#|Insert price data into SQL database
	def to_sql(self):
		if len(self.prc.index) > 0:
			sql.df_to_sql(self.prc, 'price')

	#|Convert trade data to price data
	def convert(self):

		#|Pull trade data from SQL and filter if needed
		if isinstance(self.exchange, list):
			trd = sql.trades_df(symbol=self.symbol, start=self.start)						
			trd = trd[trd['exchange'].isin(self.exchange)]
		elif self.exchange == 'all':
			trd = sql.trades_df(symbol=self.symbol, start=self.start)
		else:
			trd = sql.trades_df(exchange=self.exchange, symbol=self.symbol, 
					start=self.start)

		#|Run OLHCV conversion with appropriate 'exchange' label
		if self.name <> '':
			prc = tools.olhcv(trd, self.freq, tsmp_col='yes', 
					exchange=self.name)
		elif self.exchange == 'all' or isinstance(self.exchange, list):
			prc = tools.olhcv(trd, self.freq, tsmp_col='yes', 
					exchange='multi')
		else:
			prc = tools.olhcv(trd, self.freq, tsmp_col='yes')
		prc['source'] = 'trades'
		return prc

#|Convert bitcoin charts trade csv to price history
def bchart_csv(exchange, symbol, freq, file_path, to_sql='no'):
	trd = DataFrame.from_csv(file_path, header=None, index_col=None)
	trd.columns = ['timestamp','price','amount']
	trd = tools.date_index(trd)
	prc = tools.olhcv(trd, freq, exchange, symbol, 'yes')
	prc['source'] = 'bchart'
	if to_sql == 'yes':
		sql.df_to_sql(prc, 'price')
	return prc

#|Use since API parameter to build trade history and convert to price history
class since_history(object):

	def __init__(self, exchange, symbol, limit='', start=0):
		self.exchange = exchange
		self.symbol = symbol
		self.limit = limit
		self.i = 0
		if isinstance(start, str):			
			start = tools.dateconv(start)
		self.trd = self.build_trd(limit, start)

	#|Convert trade history into price history and insert into SQL if required
	def prc(self, freq, to_sql='no'):
		prc = tools.olhcv(self.trd, freq, tsmp_col='yes')
		prc['source'] = 'trades'
		if to_sql == 'yes':
			sql.df_to_sql(prc, 'price')
		return prc

	#|Build trade history by advancing backwards on 'since' value
	def build_trd(self, limit, start):
		trd, size = self.api_ping()
		since = int(trd.index.min()) - size
		while int(trd['timestamp'].min()) >= start and int(trd.index.min()) >= 100:
			add, size = self.api_ping(since=since)
			trd = trd.append(add)
			since = int(trd.index.min()) - size
			self.display(trd, start)
		trd['timestamp'] = trd['timestamp'].astype(int)
		trd = tools.date_index(trd)	
		return trd

	#|Ping exchange api and get trades dataframe
	def api_ping(self, since=''):
		ping = api.request(self.exchange, self.symbol,
			limit=self.limit, since=since)
		trd = ping.get()
		trd = trd.set_index('tid')
		size = len(trd.index)
		return trd, size

	#|Display last (earliest) timestamp every 10 rounds
	def display(self, trd, start):
		if self.i % 10 == 0:
			last = datetime.datetime.fromtimestamp( \
				int(trd['timestamp'].min())).strftime('%Y-%m-%d %H:%M:%S')
			goal = datetime.datetime.fromtimestamp( \
				start).strftime('%Y-%m-%d %H:%M:%S')
			print 'Last Date: %s' % last			
			print 'Goal Date: %s' % goal
			print
		self.i += 1


