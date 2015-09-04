import frmt

import json
import time as tm
from pandas import DataFrame
from urllib import urlopen

#|Run GET API request for exchange
def get(job):

    #|Set 'next' job value for trade history requests
    if job['type'] == 'trades':
        job['next'] = job['ping_limit'] + tm.time()

    #|Perform GET request
    response = urlopen(job['stmt'])
    response = json.load(response)

    if len(response) > 0:
        df = frmt.format_df(response, job)
    else:
        df = DataFrame()

    return df, job

#|Create API request statement string
def build_stmt(job):
    stmt = ''
    cmd = commands()[job['exchange']][job['symbol']]
    stmt += cmd['url']
    stmt += str('/') + cmd[job['type']]
    if 'market' in cmd.keys():
        stmt = add_parameter(stmt, 'market', job, cmd)
    if job['limit'] <> '' and 'limit' in cmd.keys():
        stmt = add_parameter(stmt, 'limit', job, cmd)
    if job['since'] <> '' and 'since' in cmd.keys():
        stmt = add_parameter(stmt, 'since', job, cmd)
    return stmt

#|Add parameter to API request string
def add_parameter(stmt, parameter, job, cmd):
    if stmt.find('?') == -1:
        stmt += str('?') + cmd[parameter] + str(job[parameter])
    else:
        stmt += str('&') + cmd[parameter] + str(job[parameter])
    return stmt

#|Individual exchange statement dictionary
def commands():

    cmd = {'bitfinex':{'btcusd':{'url':'https://api.bitfinex.com/v1',
                        'ticker':'pubticker/btcusd','trades':'trades/btcusd',
                        'limit':'limit_trades=','since':'timestamp=',
                        'stype':'timestamp'},

                    'ltcusd':{'url':'https://api.bitfinex.com/v1',
                        'ticker':'pubticker/ltcusd','trades':'trades/ltcusd',
                        'limit':'limit_trades=','since':'timestamp=',
                        'stype':'timestamp'}},

            'bitstamp':{'btcusd':{'url':'https://www.bitstamp.net/api',
                        'ticker':'ticker/', 'trades':'transactions',
                        'limit':'limit='}},

            'coinbase':{'btcusd':{'url':'https://api.exchange.coinbase.com',
                        'ticker':'products/BTC-USD/ticker','trades':'products/BTC-USD/trades',
                        'limit':'limit=','since':'before=',
                        'stype':'id'}},

            'btce':{'btcusd':{'url':'https://btc-e.com/api/3',
                        'ticker':'ticker/btc_usd','trades':'trades/btc_usd',
                        'limit':'limit='},

                    'ltcusd':{'url':'https://btc-e.com/api/3',
                        'ticker':'ticker/ltc_usd','trades':'trades/ltc_usd',
                        'limit':'limit='}},

            'btcchina':{'btccny':{'url':'https://data.btcchina.com',
                        'ticker':'data/ticker','trades':'data/historydata',
                        'limit':'limit=','since':'since=',
                        'stype':'id','market':'market=btccny'},

                    'ltccny':{'url':'https://data.btcchina.com',
                        'ticker':'data/ticker','trades':'data/historydata',
                        'limit':'limit=','since':'since=',
                        'stype':'id','market':'market=ltccny'}},

            'okcoin':{'btcusd':{'url':'https://www.okcoin.com/api/v1',
                        'ticker':'ticker.do','trades':'trades.do',
                        'since':'since=','stype':'id',
                        'market':'symbol=btc_usd'},

                    'ltcusd':{'url':'https://www.okcoin.com/api/v1',
                        'ticker':'ticker.do','trades':'trades.do',
                        'since':'since=','stype':'id',
                        'market':'symbol=ltc_usd'},

                    'btccny':{'url':'https://www.okcoin.cn/api/v1',
                        'ticker':'ticker.do','trades':'trades.do',
                        'since':'since=','stype':'id',
                        'market':'symbol=btc_cny'},

                    'ltccny':{'url':'https://www.okcoin.cn/api/v1',
                        'ticker':'ticker.do','trades':'trades.do',
                        'since':'since=','stype':'id',
                        'market':'symbol=ltc_cny'}}}

    return cmd
