import auth
import api
import tools

import csv
import codecs
import numpy as np
from pandas import DataFrame
from sqlalchemy import create_engine,  MetaData
from sqlalchemy.sql import select
from sqlalchemy import Table, Column, Integer, String, Float, DateTime

#|------------------------------------------------------
#|--------Connect to SQL data via dbconnect class-------

#|Connect to SQL database and create SQLAlchemy engine and MetaData
class dbconnect():	
	
	#|Connect to SQL database
	def __init__(self):	
		engine_str = auth.mysql()	
		self.eng = create_engine(engine_str)	
		self.conn = self.eng.connect()	
		self.meta = MetaData(self.eng)

	#|Load table variable and add to metadata
	def addtbl(self, table_name, create='no'):
		tbl = tables(self.meta, table_name)
		if create == 'yes':
			self.meta.create_all(self.eng)
		return tbl

	#|Insert DataFrame to SQL table using "INSERT OR IGNORE" command
	def df_to_sql(self, df, table_name):
		tbl = self.addtbl(table_name)		
		df = df.to_dict('records')		
		ins = tbl.insert().prefix_with('IGNORE')
		ins.execute(df)	

	#|Return DataFrame from SQL table using filter arguments
	def sql_to_df(self, table_name, exchange='', start='',
			end='', source='', freq=''):
		tbl = self.addtbl(table_name)
		sel = select([tbl])	
	
		if exchange <> '':
			sel = sel.where(tbl.c.exchange == exchange)
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

		result = self.conn.execute(sel)
		headers = result.keys()
		result = result.fetchall()
		df = DataFrame(result, columns=headers)
		df = tools.date_index(df)
		return df


#|------------------------------------------------------
#|--------Trades/Price SQL to DataFrame commands--------

#|Pull trades data from SQL table and convert to DataFrame
def trades_df(table_name, exchange='', start ='', end=''):		
	db = dbconnect()	
	trd = db.sql_to_df(table_name, exchange=exchange,
			start=start, end=end)
	return trd

#|Return price history DataFrame using exchange/source filters
def price_df(exchange='', freq='', source=''):
	db = dbconnect()
	table_name = 'price'
	prc = db.sql_to_df(table_name, exchange=exchange,
			source=source, freq=freq)
	return prc


#|------------------------------------------------------
#|----------Source specific SQL import commands---------

#|Import BitcoinCharts trade history CSV into SQL database
#|Before running, place CSV in 'modules' folder and rename file to exchange name
def import_bchart(exchange, start):
	db = dbconnect()
	trd = api.bchart(exchange, start)
	trd['exchange'] = exchange
	db.df_to_sql(trd, 'bchtrades')


#|-------------------------------------------------
#|--------------SQLAlchemy Tables------------------

#|Load SQLAlchemy table into MetaData with option to 'create'
#|SQL table in database
def tables(meta, table_name):	
	if table_name == 'api':
		tbl = Table('api', meta, Column('tid', Integer, primary_key=True),
			Column('price', Float), Column('amount', Float),
			Column('type', String(4)), Column('timestamp', Integer),
			Column('exchange', String(20)))
	if table_name == 'okcoin':
		tbl = Table(table_name, meta, Column('tid', Integer, primary_key=True),
			Column('price', Float), Column('amount', Float),
			Column('type', String(4)), Column('timestamp', Integer),
			Column('timestamp_ms', Integer), Column('exchange', String(20)))
	if table_name == 'bchart':
		tbl = Table(table_name, meta, Column('timestamp', Integer),
			Column('price', Float), Column('amount', Float),
			Column('exchange', String(20)))
	if table_name == 'price':
		tbl = Table(table_name, meta, 
			Column('timestamp', Integer, primary_key=True),
			Column('price', Float), Column('amount', Float),
			Column('open', Float), Column('high', Float),
			Column('low', Float),
			Column('freq', String(5), primary_key=True), 
			Column('exchange', String(20), primary_key=True),
			Column('source', String(3), primary_key=True))
	return tbl
