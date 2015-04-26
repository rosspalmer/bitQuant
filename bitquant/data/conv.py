# -*- coding: utf-8 -*-
import numpy as np
from pandas import DataFrame


#|Convert trades data to price data
def olhcv(trd, freq, exchange='', symbol='', label='left'):

    price = trd['price'].astype(float)
    amount = trd['amount'].astype(float)
    prc = DataFrame(index=price.resample(freq, how='last', closed='right',
                    label=label).index)

    #|Use pandas 'resample' function to create OLHCV data
    prc['open'] = price.resample(freq, how='first', closed='right',
                    label=label).fillna(value=0)
    prc['low'] = price.resample(freq, how='min', closed='right',
                    label=label).fillna(value=0)
    prc['high'] = price.resample(freq, how='max', closed='right',
                    label=label).fillna(value=0)
    prc['close'] = price.resample(freq, how='last', closed='right',
                    label=label).fillna(method='ffill')
    prc['volume'] = amount.resample(freq, how='sum', closed='right',
                    label=label).fillna(value=0)
    prc['vwap'] = ((price*amount).resample(freq, how='sum',
                    closed='right',label=label)/amount.resample(freq,
                    how='sum', closed='right', label=label)).fillna(value=0)
    prc = prc.apply(replace_zero, axis=1)

    #|Add exchange, source, and freq columns if required
    prc['freq'] = freq	
    if exchange <> '':
        prc['exchange'] = exchange
    elif 'exchange' in trd:	
        prc['exchange'] = trd['exchange'].iloc[0]
    if symbol <> '':
        prc['symbol'] = symbol
    elif 'symbol' in trd:
        prc['symbol'] = trd['symbol'].iloc[0]

    #|Add timestamp column
    prc['timestamp'] = prc.index.astype(np.int64) // 10**9

    #|Slice price data to cut off incomplete ends
    prc = prc[1:-1]
    return prc


#|Replace zeros in open, low, and high with the last close
def replace_zero(row):
    if row['open'] == 0:
        row['open'] = row['close']
        row['low'] = row['close']
        row['high'] = row['close']
        return row
    else:
        return row