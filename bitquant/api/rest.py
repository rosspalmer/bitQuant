import frmt

import json
import time as tm
from pandas import DataFrame
from urllib import urlopen

#|Run GET API request for exchange trade history
def get(values):
    values['next'] = values['ping_limit'] + tm.time()
    response = urlopen(values['stmt'])
    response = json.load(response)
    if len(response) > 0:
        df = frmt.format_df(response, values['exchange'],values['symbol'])
    else:
        df = DataFrame()
    return df, values

#|Create API request statement string
def build_stmt(values):
    stmt = ''
    cmd = commands()[values['exchange']][values['symbol']]
    stmt += cmd['url']
    stmt += str('/') + cmd['trades']
    if 'market' in cmd.keys():
        stmt = add_parameter(stmt, 'market', values, cmd)
    if values['limit'] <> '' and 'limit' in cmd.keys():
        stmt = add_parameter(stmt, 'limit', values, cmd)
    if values['since'] <> '' and 'since' in cmd.keys():
        stmt = add_parameter(stmt, 'since', values, cmd)
    return stmt

#|Add parameter to API request string
def add_parameter(stmt, parameter, values, cmd):
    if stmt.find('?') == -1:
        stmt += str('?') + cmd[parameter] + str(values[parameter])
    else:
        stmt += str('&') + cmd[parameter] + str(values[parameter])
    return stmt

#|Individual exchange statement dictionary
def commands():

    cmd = {'bitfinex':{'btcusd':{'url':'https://api.bitfinex.com/v1',
                        'trades':'trades/btcusd', 'limit':'limit_trades=',
                        'since':'timestamp=', 'stype':'timestamp'},
                    'ltcusd':{'url':'https://api.bitfinex.com/v1',
                        'trades':'trades/ltcusd','limit':'limit_trades=',
                        'since':'timestamp=', 'stype':'timestamp'}},
            'bitstamp':{'btcusd':{'url':'https://www.bitstamp.net/api',
                        'trades':'transactions','limit':'limit='}},
            'coinbase':{'btcusd':{'url':'https://api.exchange.coinbase.com',
                        'trades':'products/BTC-USD/trades','limit':'limit=',
                        'since':'before=', 'stype':'id'}},
            'btce':{'btcusd':{'url':'https://btc-e.com/api/3',
                        'trades':'trades/btc_usd','limit':'limit='},
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
