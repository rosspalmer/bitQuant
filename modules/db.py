import auth
import api
import sql
from tools import date_index, time_series, seconds

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

#|Pull trade data from SQL table and convert to DataFrame
def trades_df(table_name, exchange='', start ='', end=''):		
	eng, conn, meta = dbconnect()	
	tbl = sql.tables(meta, table_name)
	sel = select([tbl])	
	if exchange <> '':
		sel = sel.where(tbl.c.exchange == exchange)
	if start <> '':
		start = dateconv(start)
		sel = sel.where(tbl.c.timestamp >= start)
	if end <> '':
		end = dateconv(end)
		sel = sel.where(tbl.c.timestamp <= end)
	print 'select statement crafted'
	result = conn.execute(sel)
	result = result.fetchall()
#	df = date_index(df)
	return result

#|Append DataFrame to SQL table via "INSERT OR IGNORE" command
def add_to_db(df, table):
	df = df.to_dict('records')		
	ins = table.insert().prefix_with('IGNORE')	
	ins.execute(df)	

#|Import BitcoinCharts trade history CSV into SQL database
#|Before running, place CSV in 'modules' folder and rename file to exchange name
def import_bcharttrades(exchange):
	eng, conn, meta = dbconnect()	
	table = sql.tables(meta, 'bcharttrades')	
	df = DataFrame()
	path = '%s.csv' % exchange
	df = df.from_csv(path)
	df.columns = ['price','amount']
	df['timestamp'] = df.index
	df['exchange'] = exchange	
	add_to_db(df, table)

#|"Ping" exchange API for trade data and import into SQL database
def trades_ping(exchange, limit=50):
	eng, conn, meta = dbconnect()
	table = sql.tables(meta, 'trades')	
	df, ping = api.trades(exchange, limit)
	add_to_db(df, table)

#|Convert and add trade history to SQL database
def trades_to_pricedb(df, typ, exchange, source):
	table_name = "pricehistory" + str(typ)
	eng, conn, meta = dbconnect()
	table = sql.tables(meta, table_name)
	ts = time_series(df, seconds(typ=typ))
	ts['exchange'] = exchange
	ts['source'] = source	
	add_to_db(ts, table)

#|Return price history DataFrame using exchange/source filters
def price_db(typ, exchange, source):
	table_name = 'pricehistory' + str(typ)
	eng, conn, meta = dbconnect()
	tbl = sql.tables(meta, table_name)
	sel = select([tbl]).where(tbl.c.exchange == exchange)
	sel = sel.where(tbl.c.source == source)
	result = conn.execute(sel)
	result = result.fetchall()
	df = DataFrame(result, columns=('timestamp','price','amount','high','low',
					'open','exchange','source'))
	df = date_index(df)
	return df

#|Convert datetime sting (format: mm/dd/yy) to timestamp
def dateconv(date):
	date = datetime.strptime(date, "%m/%d/%y")		
	timestamp = int(mktime(date.timetuple()))	
	return timestamp

