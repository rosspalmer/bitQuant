import db

from time import mktime
from datetime import datetime
from pandas import DataFrame

class trades(object):
	
	def __init__(self, start=''):
		if start <> '':
			start = datetime.strptime(start, "%m/%d/%y")		
			start = int(mktime(start.timetuple()))	
		self.start = start
		self.df = DataFrame(columns=('tid','price','amount','type', 'exchange',
																'timestamp','timestamp_ms','dbtable'))

	def add(self, table):
		data = db.trade_data(table, start=self.start)
		data = db.date_index(data)
		data['dbtable'] = table
		self.df = self.df.append(data)
