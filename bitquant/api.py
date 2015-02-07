import tools

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

#|Import trade data from bitcoincharts API
def bchart(exchange, start):
	url = 'http://api.bitcoincharts.com/v1/trades.csv?symbol=%s&start=' % exchange	
	start = tools.dateconv(start)
	request = url + str(start)	
	response = urlopen(request)
	csvfile = csv.reader(co.iterdecode(response, 'utf-8'))
	data = list(csvfile)
	df = DataFrame(data, columns=('timestamp','price','amount')) 
	return df

#|Import daily price data from Quandl API
def quandl(exchange):
	request = 'https://www.quandl.com/api/v1/datasets/BCHARTS/%s.json' % exchange
	response = get(request)
	data = response['data']
	headers = response['column_names']
	df = DataFrame(data, columns=headers)
	return df	

#|Assigns base url string for each BTC exchange 
def urls(exchange):
	if exchange == "bitfinex":
		url = "https://api.bitfinex.com/v1"
	if exchange == "btcchina":
		url = "https://data.btcchina.com"
	if exchange == "okcoincny":
		url = "https://www.okcoin.cn/api/v1"
	if exchange == "okcoinusd":
		url = "https://www.okcoin.com/api/v1"	
	return url

#|Pulls trade data from BTC exchange API
#|'limit' is either size limit or "since" value for OKCoin exchanges
def trades(exchange, limit):
	url = urls(exchange)
	if exchange == "bitfinex":
		request = "/trades/btcusd/?limit_trades="+str(limit)
	if exchange == "btcchina":
		request = "/data/historydata?limit="+str(limit)
	if exchange == "okcoincny":
		request = "/trades.do?since="+str(limit)
	if exchange == "okcoinusd":
		request = "/trades.do?since="+str(limit)
	request = url + request
	df = get(request)
	df = json_normalize(df)	
	df = trades_format(df, exchange)	
	return df

#|Formats dataframe output of individual API trade data
#|into standard format
def trades_format(df, exchange):
	if exchange == "bitfinex":
		pass
	if exchange == "btcchina":
		df.columns = ['amount','timestamp','price','tid','type']
		df['exchange'] = 'btcchina'
	if exchange == "okcoincny":
		pass
	if exchange == "okcoinusd":
		pass
	return df

#|Pulls ticker data from exchange APIs		
def ticker(exchange):
	url = urls(exchange)
	if exchange == "bitfinex":
		request = "/pubticker/btcusd"
	if exchange == "btcchina":
		request = "/data/ticker?market=btccny"
	if exchange == "okcoincny":
		request = "/ticker.do?ok=1"
	if exchange == "okcoinusd":
		request = "/ticker.do?ok=1"	
	request = url + request
	ticker = get(request)
	return ticker
