# bitQuant v0.3.1

bitQuant is a lightweight tool for extracting and organizing Bitcoin trade data provided by exchange APIs. bitQuant is designed to standardize data from many supported exchanges and store data in either temporary **pandas** DataFrames or permanent **SQL** tables. bitQuant performs all actions using three class objects which are efficent and easy to use and are ideal for data needs of both the hobbyist and professional.

## Features

### API Class
- Request trade data from exchange REST API
- Return trade data as DataFrame
- Automatically limit rate on **ALL** requests
- Use `auto_since` feature to automatically minimize size of data requests (_currently broken_)

### SQL Class
- Automatically create SQL tables for trade and price data
- **Insert** or **select** data from SQL database using single command

### Data Class
- Combines API and SQL classes for easily extract and process data
- Convert trade history data to OLHCV price data
- Embedded DataFrames store duplicate-free trade and price data
- Use `run_loop` function to continuously perform trade data requests on multiple exchanges

### Supported Exchanges

- bitfinex
- bitstamp
- coinbase
- btce
- okcoin
- btcchina

### Supported SQL Types
- sqlite
- MySQL

## Planned Features
- Customizeable Kivy-based GUI with features below
    - Multi Exchange ticker
    - Live trade history compiling multiple exchanges
    - Live order book
- Expand API data requests to support ticker, orderbook, and lendbook data
- Add data remediation feature to fill in trade history holes using `since` API parameter
- Portfilo related API POST requests to perform trades, post orders, and access account information
- WebSocket API support to live steam data
- Support for OKCoin futures markets
- Support for additional SQL flavors

## [Documentation](https://github.com/rosspalmer/bitQuant/wiki)

## Installation and Setup Guide

Install bitQuant using source distribution from GitHub.

    git clone https://github.com/rosspalmer/bitQuant.git
    cd bitQuant
    python setup.py install

Navigate to the folder location in which you would like to keep your **login text file** and **sqlite** database (if applicable). You will need to navigate to this location to access the **login text file** in the future.

Run `setup_sql` command to setup up SQL database and tables.

    >> import bitquant as bq
    >> bq.setup_sql()

    -----SQL Database setup-----

    =Select SQL type=
      (1) sqlite
      (2) MySQL

Select the SQL type and input the relevant login information.

## License

The MIT License (MIT)

Copyright (c) 2014-2015 Ross Palmer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
