import auth
import api
import sql

from pandas import DataFrame
from pandas.io.sql import read_sql_query 
from pandas.tseries.tools import to_datetime
from sqlalchemy import create_engine,  MetaData

def dbconnect():	
	engine_str = auth.mysql()	
	eng = create_engine(engine_str)	
	conn = eng.connect()	
	meta = MetaData(eng)
	return eng, conn, meta

def trades_df(table_name, exchange='', start ='', end=''):		
	eng, conn, meta = dbconnect()	
	table = sql.tables(meta, table_name)	
	arg = {'exchange':exchange, 'start':start, 'end':end}	
	select = sql.sqlselect(table, arg)
	select = select.statement()		
	df = read_sql_query(select, eng) 
	df = date_index(df)
	return df

def add_to_db(df, table):	
	df = df.to_dict('records')		
	ins = table.insert().prefix_with('IGNORE')	
	ins.execute(df)	

def date_index(df):
	date = df['timestamp']
	date = to_datetime(date, unit='s')
	df['date'] = date
	df = df.set_index('date')
	return df

def import_bcharttrades(exchange):
	table = tables('bcharttrades')	
	df = DataFrame()
	path = '%s.csv' % exchange
	df = df.from_csv(path)
	df.columns = ['price','amount']
	df['timestamp'] = df.index
	df['exchange'] = exchange	
	add_to_db(df, table)

def trades_ping(exchange, limit=50):
	eng, conn, meta = dbconnect()
	table = sql.tables(meta, 'trades')	
	df, ping = api.trades(exchange, limit)
	add_to_db(df, table)

