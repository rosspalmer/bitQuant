import auth
import api

from pandas import DataFrame
from pandas.io.sql import read_sql 
from pandas.tseries.tools import to_datetime
from sqlalchemy import create_engine,  MetaData
from sqlalchemy import Table, Column, Integer, String, Float
from time import mktime
from datetime import datetime

engine_str = auth.mysql()
eng = create_engine(engine_str)
conn = eng.connect()
meta = MetaData(eng)

def trade_data(ntable, exchange='', date =''):
	if exchange == '' and date =='':
		df = read_sql('SELECT * FROM %s;' % (ntable,), eng)	
	elif date =='':
		df = read_sql('SELECT * FROM %s WHERE exchange = "%s";' % (ntable,exchange), eng)
	else:
		date = datetime.strptime(date, "%m/%d/%y")		
		timestamp = int(mktime(date.timetuple()))	
		df = read_sql('SELECT * FROM %s WHERE timestamp >= %s;' % (ntable, timestamp), eng)
	df = date_index(df)
	return df

def add_to_db(df, table):	
	df = df.to_dict('records')
	print '--Converted to Dictionary--'		
	ins = table.insert().prefix_with('IGNORE')	
	ins.execute(df)	
	print '--Executed--'

def date_index(df):
	date = df['timestamp']
	date = to_datetime(dt, unit='s')
	df['date'] = date
	df = df.set_index('date')
	return df

def import_csv(exchange):
	table = tables('pricehis')	
	df = DataFrame()
	path = '%s.csv' % exchange
	df = df.from_csv(path)
	df.columns = ['price','amount']
	df['timestamp'] = df.index
	df['exchange'] = exchange	
	print '--CSV Imported--'	
	add_to_db(df, table)

def trades_ping(exchange, table, limit=50):
	df, ping = api.trades(exchange, limit)
	add_to_db(df, table)

def tables(typ,create='no'):	
	if typ == 'trades':
		table = Table('tds', meta, Column('tid', Integer, primary_key=True),
			Column('price', Float), Column('amount', Float),
			Column('type', String(4)), Column('timestamp', Integer),
			Column('exchange', String(20)))
	if typ == 'oktrades':
		table = Table('oktrades', meta, Column('tid', Integer, primary_key=True),
			Column('price', Float), Column('amount', Float),
			Column('type', String(4)), Column('timestamp', Integer),
			Column('timestamp_ms', Integer), Column('exchange', String(20)))
	if typ == 'pricehis':
		table = Table('pricehis', meta, Column('timestamp', Integer),
			Column('price', Float), Column('amount', Float),
			Column('exchange', String(20)))
	if create == 'yes':
		meta.create_all(eng)
	return table

