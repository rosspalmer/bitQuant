import auth
import api
import sql

from pandas import DataFrame
from pandas.io.sql import read_sql_query 
from pandas.tseries.tools import to_datetime
from sqlalchemy import create_engine,  MetaData

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
	table = sql.tables(meta, table_name)	
	arg = {'exchange':exchange, 'start':start, 'end':end}	
	select = sql.sqlselect(table, arg)
	select = select.statement()		
	df = read_sql_query(select, eng) 
	df = date_index(df)
	return df

#|Append DataFrame to SQL table via "INSERT OR IGNORE" command
def add_to_db(df, table):
	df = df.to_dict('records')		
	ins = table.insert().prefix_with('IGNORE')	
	ins.execute(df)	

#|Create datetime index for DataFrame using "timestamp" column
def date_index(df):
	date = df['timestamp']
	date = to_datetime(date, unit='s')
	df['date'] = date
	df = df.set_index('date')
	return df

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

