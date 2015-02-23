import sql
import tools

import json
from pandas.io.json import json_normalize
from pandas import DataFrame
from urllib import urlopen

#|Request class for exchange API data
class request(object):

	def __init__(self, exchange, symbol, limit='', since=''):
		self.values = {'exchange':exchange, 'symbol':symbol,
			       'limit':limit, 'since':since}		
		self.cmd = self.commands()[exchange][symbol]
		self.stmt = ''
	
	#|Build statement for API request
	def build_stmt(self, typ):
		self.stmt = ''		
		if typ == 'trades':
			self.stmt += self.cmd['url']
			self.stmt += str('/') + self.cmd['trades']
			if 'market' in self.cmd.keys():
				self.values['market'] = ''
				self.add_parameter('market')
			if self.values['limit'] <> '' and 'limit' in self.cmd.keys():
				self.add_parameter('limit')
			if self.values['since'] <> '' and 'since' in self.cmd.keys():
				self.add_parameter('since')
		if typ == 'quandl' and 'quandl' in self.cmd.keys():
			self.stmt += 'https://www.quandl.com/api/v1/datasets/%s.json'\
					% self.cmd['quandl']
		print self.stmt

	#|Add a parameter to the API request statement
	def add_parameter(self, parameter):
		if self.stmt.find('?') == -1:
			self.stmt += str('?') + self.cmd[parameter] + str(self.values[parameter])
		else:
			self.stmt += str('&') + self.cmd[parameter] + str(self.values[parameter])

	#|GET API request and return DataFrame
	def get(self, typ='trades'):
		if self.stmt == '':
			self.build_stmt(typ)
		response = urlopen(self.stmt)
		response = json.load(response)
		if typ == 'quandl':
			df = resp_quandl(response)
		else: 
			df = resp_trades(response, self.values['exchange'])
		df = tools.standard_columns(df)
		if 'exchange' not in df:
			df['exchange'] = self.values['exchange']
		if 'symbol' not in df:
			df['symbol'] = self.values['symbol']
		return df

	#|Get data and insert into SQL database
	def to_sql(self):
		df = self.get('trades')
		sql.df_to_sql(df, 'trades')
		return df
		
	#|Individual command dictionary for exchange/symbols
	def commands(self):

		cmd = {'bitfinex':{'btcusd':{'url':'https://api.bitfinex.com/v1',
			   		     'trades':'trades/btcusd','limit':'limit_trades=',
					     'quandl':'BCHARTS/BITFINEXUSD','bchart':'bitfinexUSD'},
				   'ltcusd':{'url':'https://api.bitfinex.com/v1',
					     'trades':'trades/ltcusd','limit':'limit_trades='}},
		       'bitstamp':{'btcusd':{'url':'https://www.bitstamp.net/api',
					     'trades':'transactions','quandl':'BCHARTS/BITSTAMPUSD',
					     'bchart':'bitstampUSD'}},
		       'btce':{'btcusd':{'url':'https://btc-e.com/api/3',
					 'trades':'trades/btc_usd','limit':'limit=',
					 'quandl':'BCHARTS/BTCEUSD','bchart':'btceUSD'},
			       'ltcusd':{'url':'https://btc-e.com/api/3',
					 'trades':'trades/ltc_usd','limit':'limit='}},
		       'btcchina':{'btccny':{'url':'https://data.btcchina.com',
					     'trades':'data/historydata','limit':'limit=',
					     'since':'since=','market':'market=btccny',
					     'bchart':'btcnCNY'},
				   'ltccny':{'url':'https://data.btcchina.com',
					     'trades':'data/historydata','limit':'limit=',
					     'since':'since=','market':'market=ltccny'}},
		       'okcoin':{'btcusd':{'url':'https://www.okcoin.com/api/v1',
					   'trades':'trades.do','since':'since=',
			    		   'market':'symbol=btc_usd'},
				 'ltcusd':{'url':'https://www.okcoin.com/api/v1',
					   'trades':'trades.do','since':'since=',
			    		   'market':'symbol=ltc_usd'},
				 'btccny':{'url':'https://www.okcoin.cn/api/v1',
					   'trades':'trades.do','since':'since=',
			    		   'market':'symbol=btc_cny'},
				 'ltccny':{'url':'https://www.okcoin.cn/api/v1',
					   'trades':'trades.do','since':'since=',
			    		   'market':'symbol=ltc_cny'}}}
		return cmd

#|Convert Quandl API response to DataFrame
def resp_quandl(response):
	data = response['data']
	headers = response['column_names']
	df = DataFrame(data, columns=headers)
	df['timestamp'] = df['Date'].apply(tools.dateconv)
	df = tools.date_index(df.drop('Date', axis=1))
	return df

#|Convert Exchange API response to DataFrame
def resp_trades(response, exchange):
	if exchange == 'btce':
		for col in response:
			response = response[col]
	df = json_normalize(response)
	return df


