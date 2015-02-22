import auth
import tools

import numpy as np
from pandas import DataFrame
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine,  MetaData
from sqlalchemy.sql import select
from sqlalchemy import Table, Column, Integer, String, Float, DateTime
from sqlalchemy.sql.expression import delete

#|Create all tables in MySQL database
def setup_tables():
	db = dbconnect()
	db.add_tbl('trades')
	db.add_tbl('price')
	db.add_tbl('exchanges',create='yes')

#|------------------------------------------------------
#|--------Connect to SQL data via dbconnect class-------

#|Connect to SQL database and create SQLAlchemy engine and MetaData
class dbconnect():	
	
	#|Connect to SQL database
	def __init__(self):	
		engine_str = auth.sql()
		if engine_str.find('sqlite') == 0:
			self.sql = 'sqlite'
			self.eng = create_engine(engine_str, module=sqlite)
		else:
			self.sql = 'mysql'
			self.eng = create_engine(engine_str)
		self.conn = self.eng.connect()	
		self.meta = MetaData(self.eng)

	#|Load table variable and add to metadata
	def add_tbl(self, table_name, create='no'):
		tbl = self.tables(table_name)
		if create == 'yes':
			self.meta.create_all(self.eng)
		return tbl

	#|Insert DataFrame to SQL table using types
	#|(i) INSERT OR INGORE (d) Delete and insert
	def df_to_sql(self, df, table_name, typ):
		tbl = self.add_tbl(table_name)		
		data = df.to_dict('records')		
		if typ == 'i':
			stmt = self.sql_insert(tbl)
		if typ == 'd':
			stmt = tbl.delete()
			stmt.execute()
			stmt = self.sql_insert(tbl)
		stmt.execute(data)

	#Customize insert or ignore command for different SQLs
	def sql_insert(self, tbl):
		if self.sql == 'mysql':
			stmt = tbl.insert().prefix_with('IGNORE')
		if self.sql == 'sqlite':
			stmt = tbl.insert().prefix_with('OR IGNORE')
		return stmt

	#|Return DataFrame from SQL table using filter arguments
	def sql_to_df(self, table_name, exchange='',  symbol='',
			start='', end='', source='', freq=''):
		tbl = self.add_tbl(table_name)
		sel = select([tbl])	
	
		#|Build select statement using input parameters
		if exchange <> '':
			sel = sel.where(tbl.c.exchange == exchange)
		if symbol <> '':
			sel = sel.where(tbl.c.symbol == symbol)
		if start <> '':
			if isinstance(start, str):			
				start = tools.dateconv(start)
			sel = sel.where(tbl.c.timestamp >= start)
		if end <> '':
			if isinstance(end, str):
				end = tools.dateconv(end)
			sel = sel.where(tbl.c.timestamp <= end)
		if source <> '':
			sel = sel.where(tbl.c.source == source)
		if freq <> '':
			sel = sel.where(tbl.c.freq == freq)

		#|Request data from MySQL server and format
		result = self.conn.execute(sel)
		headers = result.keys()
		result = result.fetchall()
		df = DataFrame(result, columns=headers)
		#|Create datetime index if data has 'timestamp' column		
		try:		
			df = tools.date_index(df)
		except:
			pass
		return df
	
	#|Load SQLAlchemy table into MetaData with option to 'create'
	#|SQL table in database
	def tables(self, table_name):	

		if table_name == 'trades':
			tbl = Table(table_name, self.meta, Column('tid', Integer, primary_key=True),
				Column('price', Float), Column('amount', Float),
				Column('type', String(4)), Column('timestamp', Integer),
				Column('timestamp_ms', Integer), 
				Column('exchange', String(20), primary_key=True),
				Column('symbol', String(6), primary_key=True))
		if table_name == 'price':
			tbl = Table(table_name, self.meta,
				Column('timestamp', Integer, primary_key=True),
				Column('exchange', String(20), primary_key=True),
				Column('symbol', String(6), primary_key=True),
				Column('freq', String(5), primary_key=True),
				Column('open', Float), Column('low', Float),
				Column('high', Float), Column('close', Float),
				Column('volume', Float),
				Column('source', String(10), primary_key=True))
		if table_name == 'exchanges':
			tbl = Table(table_name, self.meta,
				Column('exchange', String(20), primary_key=True),
				Column('symbol', String(6), primary_key=True),
				Column('url', String(50)), Column('trade', String(50)),
				Column('limit', String(20)), Column('since', String(20)),
				Column('market', String(20)),Column('quandl', String(50)), 
				Column('bchart', String(20)),Column('last_touch', Integer))
		return tbl

#|----------------------------------------------------
#|--------Shortcut SQL <--> DataFrame commands--------

#|Insert (or Ignore) Dataframe into SQL database
def df_to_sql(df, table_name, typ='i'):
	db = dbconnect()
	db.df_to_sql(df, table_name, typ)

#|Return trades data from SQL as DataFrame
def trades_df(exchange='', symbol='', start ='', end=''):		
	db = dbconnect()	
	df = db.sql_to_df('trades', exchange=exchange,
			symbol=symbol, start=start, end=end)
	return df

#|Return price history from SQL using exchange/source filters as DataFrame
def price_df(exchange='', freq='', source='',start=''):
	db = dbconnect()
	df = db.sql_to_df('price', exchange=exchange, freq=freq,
			source=source, start=start)
	return df

#|Return exchange information table from SQL as DataFrame
def exchanges_df(exchange='', symbol=''):
	db = dbconnect()
	df = db.sql_to_df('exchanges',
		exchange=exchange, symbol=symbol)
	return df
	
