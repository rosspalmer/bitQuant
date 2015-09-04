import numpy as np
from pandas.io.json import json_normalize
from pandas import DataFrame, to_datetime

#|Create DataFrame from JSON response and standardize data
def format_df(response, job):

    if job['type'] == 'trades':
        if job['exchange'] == 'btce':
            for col in response:
                response = response[col]
        df = json_normalize(response)
        if job['exchange'] == 'coinbase':
            df['time'] = to_datetime(df['time'], utc=0)
            df['timestamp'] = df['time'].astype(np.int64) // 10**9
    else:
        df = json_normalize(response)

    df = standard_columns(df)

    if 'exchange' not in df:
        df['exchange'] = job['exchange']
    if 'symbol' not in df:
        df['symbol'] = job['symbol']
    return df

#|Standardize column names and drop columns not in dictionary below
def standard_columns(df):
    cols = []
    headers = {'tid':'tid','trade_id':'tid',
        'price':'price',
        'amount':'amount','size':'amount',
        'type':'type','side':'type',	
        'timestamp':'timestamp','date':'timestamp',
        'timestamp_ms':'timestamp_ms','date_ms':'timestamp_ms',
        'volume':'volume',
        'exchange':'exchange',
        'Open':'open',
        'Low':'low',
        'High':'high',
        'Close':'close',
        'Volume (BTC)':'volume',
        'Weighted Price':'vwap',
        'source':'source',
        'freq':'freq',
        'ask':'ask','btc_usd.buy':'ask','ltc_usd.buy':'ask','ticker.sell':'ask',
        'bid':'bid','btc_usd.sell':'bid','ltc_usd.sell':'bid','ticker.buy':'bid',
        'high':'high','btc_usd.high':'high','ltc_usd.high':'high','ticker.high':'high',
        'low':'low','btc_usd.low':'low','ltc_usd.low':'low','ticker.low':'low',
        'last_price':'last','btc_usd.last':'last','ltc_usd.last':'last','ticker.last':'last'}

    for col in df:
        if col in headers.keys():
            cols.append(headers[col])
        else:
            df = df.drop(col, axis=1)
    df.columns = cols
    return df

