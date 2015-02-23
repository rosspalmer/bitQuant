# bitQuant v0.2.1

The goal of bitQuant is to provide a complete package for gathering Bitcoin trade data, backtesting trade algorithms, and implementing those algorithms live. bitQuant is designed to be as efficient as possible to suite the needs of both the hobbist and the professional, and is compatible with multiple Bitcoin exchanges.

###Data
- "Ping" exchange APIs for trade history data
- Convert trade history to OLHCV price history at any frequency
- Store trade or price history data from exchange APIs in MySQL server
- Automatically maintain and update MySQL server through cron job scripts
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

**(1a) Install via PyPi**

  `easy_install bitquant` or `pip install bitquant`

**(1b) Install `setup.py` the hard way**

    python setup.py install

**(2) Setup SQL database**

Run SQL setup script, choose sqlite or MySQL

    >> import bitquant as bq
    >> bq.auth.sql_setup()

**(3) Upload default exchange API command library and create MySQL tables**

    >> bq.sql.setup_tables()
    >> bq.api.set_default()

##Quickstart API Guide

    >> import bitquant as bq

###Add Data to MySQL database

Insert DataFrame into MySQL table

    >> bq.df_to_sql(df, table_name, typ='i'):

Ping exchange API for trade history data, insert data, and return DataFrame

    >> ping = bq.trades_api(exchange, symbol, limit='', since='')
    >> trade_history = ping.to_sql()

Convert trade history to OLHCV price history, insert data, and return DataFrame

    >> top = bq.trades_to_price(exchange, symbol, freq, start)
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

    >> c.run(length)

##Variables

**`exchange`: exchange name (supported)**
- `bitfinex`
- `bitstamp`
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
