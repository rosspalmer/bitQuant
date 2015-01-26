import auth
import api
import sql
import tools
#from tools import date_index, time_series, seconds, dateconv

from pandas import DataFrame
from sqlalchemy import create_engine,  MetaData
from sqlalchemy.sql import select

#|Connect to SQL database and create SQLAlchemy engine and MetaData
def dbconnect():	
	engine_str = auth.mysql()	
	eng = create_engine(engine_str)	
	conn = eng.connect()	
	meta = MetaData(eng)
	return eng, conn, meta

#|----------------------------------------
#|-----Generic SQL-DataFrame commands-----

#|Insert DataFrame to SQL table using "INSERT OR IGNORE" command
def df_to_sql(df, table):
	df = df.to_dict('records')		
	ins = table.insert().prefix_with('IGNORE')	
	ins.execute(df)	

#|Return DataFrame from SQL table using filter arguments
def sql_to_df(table_name, exchange='', start='',
		end='', source=''):
	eng, conn, meta = dbconnect()
	tbl = sql.tables(meta, table_name)
	sel = select([tbl])	
	
	if exchange <> '':
		sel = sel.where(tbl.c.exchange == exchange)
	if start <> '':
		start = tools.dateconv(start)
		sel = sel.where(tbl.c.timestamp >= start)
	if end <> '':
		end = tools.dateconv(end)
		sel = sel.where(tbl.c.timestamp <= end)
	if source <> '':
		sel = sel.where(tbl.c.source == source)
	
	result = conn.execute(sel)
	headers = result.keys()
	result = result.fetchall()
	df = DataFrame(result, columns=headers)
	df = tools.date_index(df)
	return df

#|-----------------------------------------------
#|-----Trade/Price SQL to DataFrame commands-----
#| ~~ Used to force required variable inputs ~~

#|Pull trade data from SQL table and convert to DataFrame
def trades_df(table_name, exchange='', start ='', end=''):		
	df = sql_to_df(table_name, exchange=exchange,
			start=start, end=end)
	return df

#|Return price history DataFrame using exchange/source filters
#|available "typ" options are 'm'(min), 'h'(hour), or 'd'(day)
def price_df(typ, exchange, source):
	table_name = 'pricehistory' + str(typ)
	df = sql_to_df(table_name, exchange=exchange,
			source=source)
	return df

#|---------------------------------------------
#|-----Source specific SQL import commands-----

#|"Ping" exchange API for trade data and import into SQL database
def trades_api_ping(exchange, limit=50):
	eng, conn, meta = dbconnect()
	tbl = sql.tables(meta, 'trades')	
	df, ping = api.trades(exchange, limit)
	df_to_sql(df, tbl)

#|Convert trade history to price and add to SQL database
def trades_to_pricedb(df, typ, exchange, source):
	table_name = "pricehistory" + str(typ)
	eng, conn, meta = dbconnect()
	tbl = sql.tables(meta, table_name)
	ts = tools.time_series(df, seconds(typ=typ))
	ts['exchange'] = exchange
	ts['source'] = source	
	df_to_sql(ts, tbl)

#|Import BitcoinCharts trade history CSV into SQL database
#|Before running, place CSV in 'modules' folder and rename file to exchange name
def import_bcharttrades(exchange):
	eng, conn, meta = dbconnect()	
	tbl = sql.tables(meta, 'bcharttrades')	
	df = DataFrame()
	path = '%s.csv' % exchange
	df = df.from_csv(path)
	df.columns = ['price','amount']
	df['timestamp'] = df.index
	df['exchange'] = exchange	
	df_to_sql(df, tbl)


