import frmt

import json
import time as tm
from urllib import urlopen

def get(values):
    values['next'] = values['ping_limit'] + tm.time()
    response = urlopen(values['stmt'])
    response = json.load(response)
    df = frmt.format_df(response, values['exchange'],
                values['symbol'], values['mode'])
    return df, values

def build_stmt(values):
    stmt = ''
    cmd = commands()[values['exchange']][values['symbol']]
    if values['mode'] == 'trades':
        stmt += cmd['url']
        stmt += str('/') + cmd['trades']
        if 'market' in cmd.keys():
            stmt = add_parameter(stmt, 'market', values, cmd)
        if values['limit'] <> '' and 'limit' in cmd.keys():
            stmt = add_parameter(stmt, 'limit', values, cmd)
        if values['since'] <> '' and 'since' in cmd.keys():
            stmt = add_parameter(stmt, 'since', values, cmd)
    if values['mode'] == 'quandl' and 'quandl' in cmd.keys():
        stmt += 'https://www.quandl.com/api/v1/datasets/%s.json'\
                        % cmd['quandl']
    return stmt

def add_parameter(stmt, parameter, values, cmd):
    if stmt.find('?') == -1:
        stmt += str('?') + cmd[parameter] + str(values[parameter])
    else:
        stmt += str('&') + cmd[parameter] + str(values[parameter])
    return stmt

def commands():

    cmd = {'bitfinex':{'btcusd':{'url':'https://api.bitfinex.com/v1',
                        'trades':'trades/btcusd', 'limit':'limit_trades=',
                        'since':'timestamp=', 'stype':'timestamp',
                        'quandl':'BCHARTS/BITFINEXUSD', 'bchart':'bitfinexUSD'},
                    'ltcusd':{'url':'https://api.bitfinex.com/v1',
                        'trades':'trades/ltcusd','limit':'limit_trades=',
                        'since':'timestamp=', 'stype':'timestamp'}},
            'bitstamp':{'btcusd':{'url':'https://www.bitstamp.net/api',
                        'trades':'transactions','limit':'limit=',
                        'quandl':'BCHARTS/BITSTAMPUSD', 'bchart':'bitstampUSD'}},
            'coinbase':{'btcusd':{'url':'https://api.exchange.coinbase.com',
                        'trades':'products/BTC-USD/trades','limit':'limit=',
                        'since':'before=', 'stype':'id'}},
            'btce':{'btcusd':{'url':'https://btc-e.com/api/3',
                        'trades':'trades/btc_usd','limit':'limit=',
                        'quandl':'BCHARTS/BTCEUSD','bchart':'btceUSD'},
                    'ltcusd':{'url':'https://btc-e.com/api/3',
                        'trades':'trades/ltc_usd','limit':'limit='}},
            'btcchina':{'btccny':{'url':'https://data.btcchina.com',
                        'trades':'data/historydata','limit':'limit=',
                        'since':'since=', 'stype':'id',
                        'market':'market=btccny'},
                    'ltccny':{'url':'https://data.btcchina.com',
                        'trades':'data/historydata','limit':'limit=',
                        'since':'since=', 'stype':'id',
                        'market':'market=ltccny'}},
            'okcoin':{'btcusd':{'url':'https://www.okcoin.com/api/v1',
                        'trades':'trades.do','since':'since=',
                        'stype':'id', 'market':'symbol=btc_usd'},
                    'ltcusd':{'url':'https://www.okcoin.com/api/v1',
                        'trades':'trades.do','since':'since=',
                        'stype':'id', 'market':'symbol=ltc_usd'},
                    'btccny':{'url':'https://www.okcoin.cn/api/v1',
                        'trades':'trades.do','since':'since=',
                        'stype':'id', 'market':'symbol=btc_cny'},
                    'ltccny':{'url':'https://www.okcoin.cn/api/v1',
                        'trades':'trades.do','since':'since=',
                        'stype':'id', 'market':'symbol=ltc_cny'}}}

    return cmd
