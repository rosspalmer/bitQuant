import api
import sql

import datetime
import pandas as pd
from abc import ABCMeta, abstractmethod

#|Quandl API data handler
class quandl_dh(object):

	def __init__(self, sym_list):
		self.sym_list = sym_list
		self.data = {}
		self.build_data()

	def build_data(self):
		for sym in self.sym_list:
			self.data[sym] = api.quandl(sym)
			self.data[sym].index = self.data[sym]['Date']
			self.data[sym] = self.data[sym].drop('Date',axis=1)
	
	def lags(self, column_name, lags=1, size=1):
		for sym in self.sym_list:
			self.data[sym] = add_lags(self.data, column_name,
					lags, size)
	

#|Data handler for MySQL price data
class sql_dh(object):
	
	def __init__(self, sym_list, freq, source):
		self.sym_list = sym_list
		self.data = {}
		self.freq = freq
		self.source = source		
		self.build_data()

	def build_data(self):
		db = sql.dbconnect()
		for sym in self.sym_list:
			self.data[sym] = db.sql_to_df('price',exchange=sym,
					freq=self.freq,source=self.source)
			self.data[sym] = self.data[sym].drop(['exchange','freq','source'],axis=1)

	def lags(self, column_name, lags=1, size=1):
		for sym in self.sym_list:
			self.data[sym] = add_lags(self.data, column_name,
					lags, size)

#|Add laged series of specific column
def add_lags(data, column_name, lags, size):
	for i in range(lags):
		lag_name = '%s lag%s' % (column_name, str(i+1))
		data[lag_name] = data[column_name].shift((i+1)*size)
	data = data.dropna()
