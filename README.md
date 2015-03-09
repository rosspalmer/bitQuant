# bitQuant v0.2.8

The goal of bitQuant is to provide a complete package for gathering Bitcoin trade data, backtesting trade algorithms, and implementing those algorithms live. bitQuant is designed to be as efficient as possible to suite the needs of both the hobbist and the professional, and is compatible with multiple Bitcoin exchanges.

###Data
- "Ping" exchange APIs for trade history data
- Convert trade history to OLHCV price history at any frequency
- Store trade or price history data from in SQL server
- Automatically maintain and update SQL data
- Quandl API access for EOD data
- BitcoinCharts csv file support

###Backtest (in development)
- Backtest trading algorithms against collected data
- Event driven backtester
- Easy intergration of indicators and strategies

###Live (in planning)
- Run trading algorithms live for multiple exchanges
- Compatiable with backtest algorithms

##Installation

**(1) Install via PyPi**

  `easy_install bitquant`

**(2) Configure SQL database**

Run SQL access setup and create SQL tables

Supported: sqlite MySQL

    >> import bitquant as bq
    >> bq.sql.setup()

##Tutorials

- **[Basics](https://github.com/rosspalmer/bitQuant/wiki/Tutorial---Basics)**
- **[Data Maintenance](https://github.com/rosspalmer/bitQuant/wiki/Tutorial---Data-Maintenance)**

##Speed test

Most data interactions are instantaneous but I wanted to test the module with a very large dataset.

The `bchart_csv` function will upload a 800MB [csv file](http://api.bitcoincharts.com/v1/csv/) from BitcoinCharts which contains the complete BTCChina trades history of over 18 million trades (ie. rows).

The data is then converted to OLHCV price history with a 30 min period.

Finally, the price history is inserted into a low-budget remote low-budget MySQL server ~1,000 miles away.

The whole process took only 26 seconds.

    **Total time: 25.9832 s**
    File: data.py
    Function: bchart_csv at line 32

    Line #      Hits         Time  Per Hit   % Time  Line Contents
    ==============================================================
        32                                           @profile
        33                                           def bchart_csv(exchange, symbol, freq, file_path,
        34         1      6.80763 6807633.0     26.2  	trd = DataFrame.from_csv(file_path, header=None,
        35         1           49     49.0      0.0  	print len(trd.index)
        36         1          129    129.0      0.0  	trd.columns = ['timestamp','price','amount']
        37         1      2.03429 2034294.0     7.8  	trd = tools.date_index(trd)
        38         1      7.09359 7093593.0     27.3  	prc = tools.olhcv(trd, freq, exchange, symbol, 'yes')
        39         1         3316   3316.0      0.0  	prc['source'] = 'bchart'
        40         1            1      1.0      0.0  	if to_sql == 'yes':
        41         1     10.04414 10044148.0    38.7  		sql.df_to_sql(prc, 'price')
        42         1            3      3.0      0.0  	return prc

##Variables

**`exchange`: exchange name (supported)**
- `bitfinex`
- `bitstamp`
- `coinbase`
- `btce`
- `okcoin`
- `btcchina`

**`symbol`: symbol name (supported)**
- `btcusd`
- `ltcusd`
- `btccny`
- `ltccny`

**`freq`: frequency of OLHCV price data**
- `min`: minute
- `xmin`: x minute (for integer x)
- `h`: hour
- `d`: day
- `m`: month

**`source`: source of trade data for price history**
- `trades`: price data converted from MySQL trade history
- `bchart`: price data converted from BitcoinChart csv file

**`job`: job type for cron class**
- `trades`: Ping API for trade data and add to MySQL (hard_time required)
- `price`: Convert trade data to price data adn add to MySQL (freq required)

**`hard_time`: time between instances of a job**
- Input integer in seconds

**`start`: start point of data set**
- Input `m/d/yy` for start date
- or input UNIX timestamp

**`end`: end point of data set**
- Input `m/d/yy` for end date
- or input UNIX timestamp

**`limit`: limit number of API response rows**
- Input integer

**`since`: pull API data starting from `since` trade id(tid)**
- Input integer

**`to_sql`: insert returned data into MySQL database**
- 'no' (default) or 'yes'

##Quickstart API Guide

    >> import bitquant as bq

###Add Data to MySQL database

Insert DataFrame into MySQL table

    >> bq.df_to_sql(df, table_name, typ='i'):

Ping exchange API for trade history data, insert data, and return DataFrame

    >> ping = bq.request(exchange, symbol, limit='', since='')
    >> trade_history = ping.to_sql()

Convert trade history to OLHCV price history, insert data, and return DataFrame

    >> top = bq.trades_to_price(exchange, symbol, freq, start=0, name='')
    >> price_history = top.to_sql()

Upload trade history csv from [BitcoinCharts](http://api.bitcoincharts.com/v1/csv/) and return price history

    >> price_history = bq.bchart_csv(exchange, symbol, freq, file_path, to_sql='no'):

###Pull Data from MySQL/Quandl as pandas DataFrame

Pull trade history data from MySQL database

    >> trade_history = bq.trades_df(exchange='', symbol='', start ='', end='')

Pull price history data from MySQL database

    >> price_history = bq.price_df(exchange='', freq='', source='',start='')

Pull EOD price history from Quandl API

    >> price_history = bq.quandl(exchange, symbol)

###Maintain MySQL servers with `cron` class

Create `cron` class

    >> c = bq.cron()

Add `job` for cron class (may add multiple jobs)

    >> c.add_job(self, exchange, symbol, job, limit='', since='', freq='', hard_time=''):

Run cron class, `length` should be the number of seconds for the cron job interval

    >> c.run(length, log='no')


