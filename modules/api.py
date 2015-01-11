from urllib import urlopen
import time as tm
import json
from pandas.io.json import json_normalize

def pull(request,typ):	
	ping = tm.time()	
	response = urlopen(request)
	data = json.load(response)
	if typ == "norm":	
		data = json_normalize(data)
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
	trades, ping = pull(request,"norm")
	trades = trades_format(trades,exchange)	
	return trades, ping
	
def trades_format(trades, exchange):
	if exchange == "bitfinex":
		pass
	if exchange == "btcchina":
		trades.columns = ['amount','timestamp','price','tid','type']
		trades['exchange'] = 'btcchina'
	if exchange == "okcoincny":
		pass
	if exchange == "okcoinusd":
		pass
	return trades
		
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
	ticker, ping = pull(request,"smp")
	return ticker, ping

