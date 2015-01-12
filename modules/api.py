from urllib import urlopen
import time as tm
import json
from pandas.io.json import json_normalize

def pull(request):	
	ping = tm.time()	
	response = urlopen(request)
	data = json.load(response)
	ping = round(tm.time() - ping,3)
	return data, ping

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
	df, ping = pull(request)
	df = json_normalize(df)	
	df = trades_format(df, exchange)	
	return df, ping
	
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
	ticker, ping = pull(request)
	return ticker, ping

