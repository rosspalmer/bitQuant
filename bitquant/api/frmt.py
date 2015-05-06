import numpy as np
from pandas.io.json import json_normalize
from pandas import DataFrame, to_datetime

def format_df(response, exchange, symbol, mode):
    if mode == 'trades':
        df = trades(response, exchange, symbol, mode)
    if mode == 'quandl':
        df = quandl(response)
    df = standard_columns(df)
    if 'exchange' not in df:
        df['exchange'] = exchange
    if 'symbol' not in df:
        df['symbol'] = symbol
    return df

def trades(response, exchange, symbol, mode):
    if exchange == 'btce':
        for col in response:
            response = response[col]
    df = json_normalize(response)
    if symbol == 'coinbase':
            df['time'] = to_datetime(df['time'], utc=0)
            df['timestamp'] = df['time'].astype(np.int64) // 10**9
    return df

def quandl(response):
    data = response['data']
    headers = response['column_names']
    df = DataFrame(data, columns=headers)
    df['timestamp'] = df['Date'].apply(tools.dateconv)
    df['freq'] = 'd'
    df['source'] = 'quandl'
    df = tools.date_index(df.drop('Date', axis=1))
    return df

def standard_columns(df):
    cols = []
    headers = {'tid':'tid','trade_id':'tid',
        'price':'price',
        'amount':'amount','size':'amount',
        'type':'type','side':'type',	
        'timestamp':'timestamp','date':'timestamp',
        'timestamp_ms':'timestamp_ms','date_ms':'timestamp_ms',
        'exchange':'exchange',
        'Open':'open',
        'Low':'low',
        'High':'high',
        'Close':'close',
        'Volume (BTC)':'volume',
        'Weighted Price':'vwap',
        'source':'source',
        'freq':'freq'}

    for col in df:
        if col in headers.keys():
            cols.append(headers[col])
        else:
            df = df.drop(col, axis=1)
    df.columns = cols
    return df

