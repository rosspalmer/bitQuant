import api
import sql

import datetime
import pandas as pd
from abc import ABCMeta, abstractmethod

class data_handler(object):
	__metaclass__ = ABCMeta

	@abstractmethod
	def latest_bars(self, sym, n=1):
		raise NotImplementedError

	def update_bars(self):
		raise NotImplementedError

#|Quandl API data handler
class quandl_dh(data_handler):

	def __init__(self, sym_list):
		self.sym_list = sym_list
		self.data = {}
		self.latest_data = {}
		self.continue_backtest = True
		self.count = 1
		self.build_data()

	#|Build dataset by pinging Quandl API for all symbols
	def build_data(self):
		for sym in self.sym_list:
			self.data[sym] = api.quandl(sym)
			self.data[sym].index = self.data[sym]['Date']
			self.data[sym] = self.data[sym].drop('Date',axis=1)
			self.latest_data[sym] = []

	def latest_bars(self, sym, n=1):
		try:
			bars_list = self.latest_data[sym]
		except KeyError:
			print 'symbol is not in data set'
		else:
			return bars_list[-N:]
	
	def update_bars(self):
		for sym in self.sym_list:
			bar = self.new_bar(sym)
			self.latest_data[sym].append(bar)
		pass		
	
	def new_bar(self, sym):
		row = self.data[sym].iloc[-self.count]
		bar = ([sym, row.name, row['Open'], row['Close'],
				row['Low'], row['High'], row['Volume (BTC)']])
		print bar
		self.count += 1		
		return

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




