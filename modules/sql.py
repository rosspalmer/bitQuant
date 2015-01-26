from sqlalchemy import Table, Column, Integer, String, Float, DateTime
from sqlalchemy import create_engine

#|Load SQLAlchemy table into MetaData with option to 'create'
#|SQL table in database
def tables(meta, table_name):	
	if table_name == 'trades':
		tbl = Table('tds', meta, Column('tid', Integer, primary_key=True),
			Column('price', Float), Column('amount', Float),
			Column('type', String(4)), Column('timestamp', Integer),
			Column('exchange', String(20)))
	if table_name == 'oktrades':
		tbl = Table(table_name, meta, Column('tid', Integer, primary_key=True),
			Column('price', Float), Column('amount', Float),
			Column('type', String(4)), Column('timestamp', Integer),
			Column('timestamp_ms', Integer), Column('exchange', String(20)))
	if table_name == 'bcharttrades':
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



