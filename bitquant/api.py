import tools
import sql

import csv
import codecs as co
from urllib import urlopen
import time as tm
import json
from pandas.io.json import json_normalize
from pandas import DataFrame

#|Generic API GET request and return JSON data
def get(request):	
	response = urlopen(request)
	data = json.load(response)
	return data

#|Ping exchange API and return DataFrame
class trades_api(object):

	def __init__(self, exchange, symbol, limit='', since=''):
		self.exchange = exchange
		self.symbol = symbol
		self.limit = limit
		self.since = since
		self.exc = sql.exchanges_df(exchange=exchange,symbol=symbol)
		self.exc = self.exc.iloc[0]

	#|Build request statement, ping exchange API, 
	#|format GET data, and return DataFrame
	def get_data(self):
		request = self.trades_statement()
		df = get(request)
		df = self.format_data(df)
		return df

	#|Insert trades data into
	def to_sql(self):
		df = self.get_data()
		sql.df_to_sql(df, 'trades')
		return df

	#|Construct statement for API trade history data request
	def trades_statement(self):
		request = self.exc['url']
		request += str('/') + self.exc['trade']	
		if self.exc['market'] <> 'None':
			request = add_parameter(self.exc, request, 'market')
		if self.limit <> '' and self.exc['limit'] <> 'None':
			request = add_parameter(self.exc, request, 'limit', self.limit)
		if self.since <> '' and self.exc['since'] <> 'None':
			request = add_parameter(self.exc, request, 'since', self.since)
		return request

	#|Normalize data from API request, standardize column headers,
	#|and add 'exchange' and 'symbol' columns if not present
	def format_data(self, df):
		df = json_normalize(df)
		df = tools.standard_columns(df)
		if 'exchange' not in df:
			df['exchange'] = self.exchange
		if 'symbol' not in df:
			df['symbol'] = self.symbol
		return df

#|Add a parameter to the API request statement
def add_parameter(exc, request, parameter, value=''):
	if request.find('?') == -1:
		request += str('?') + exc[parameter] + str(value)
	else:
		request += str('&') + exc[parameter] + str(value)
	return request
	

#|Import daily price data from Quandl API
def quandl(sym, add_sql='no'):
	request = 'https://www.quandl.com/api/v1/datasets/%s.json' % sym
	response = get(request)
	data = response['data']
	headers = response['column_names']
	df = DataFrame(data, columns=headers)
	return df

