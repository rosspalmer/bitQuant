from time import mktime
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, Float, DateTime

#|Load SQLAlchemy table into MetaData with option to 'create'
#|SQL table in database
def tables(meta, table_name, create='no'):	
	if table_name == 'trades':
		table = Table('tds', meta, Column('tid', Integer, primary_key=True),
			Column('price', Float), Column('amount', Float),
			Column('type', String(4)), Column('timestamp', Integer),
			Column('exchange', String(20)))
	if table_name == 'oktrades':
		table = Table(table_name, meta, Column('tid', Integer, primary_key=True),
			Column('price', Float), Column('amount', Float),
			Column('type', String(4)), Column('timestamp', Integer),
			Column('timestamp_ms', Integer), Column('exchange', String(20)))
	if table_name == 'bcharttrades':
		table = Table(table_name, meta, Column('timestamp', Integer),
			Column('price', Float), Column('amount', Float),
			Column('exchange', String(20)))
	if table_name.find('pricehistory') == 0:
		table = Table(table_name, meta, 
			Column('timestamp', Integer, primary_key=True),
			Column('price', Float), Column('amount', Float),
			Column('open', Float), Column('high', Float),
			Column('low', Float), 
			Column('exchange', String(20), primary_key=True),
			Column('source', String(3), primary_key=True))	
	if create == 'yes':
		meta.create_all(eng)
	return table



