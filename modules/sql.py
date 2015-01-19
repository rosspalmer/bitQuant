from time import mktime
from datetime import datetime
from sqlalchemy import Table, Column, Integer, String, Float

#|Create custom SQL 'SELECT' command string based on values passed through
#|in 'arg' dictionary: arg => {exchange, start, end}
class sqlselect(object):
	def __init__(self, table, arg = {}):
		self.arg = arg		
		self.stmt = 'SELECT * FROM %s' % table
	
	#|Build and output statement string
	def statement(self):
		if self.arg['exchange'] == '' and self.arg['start'] =='' and self.arg['end'] =='':
			self.end()
		if self.arg['exchange'] <> '':
			self.where('exchange', '=', self.arg['exchange'])
		else:
			self.where('exchange', '=', '*')			
		if self.arg['start'] <> '':
			self.andwhere('timestamp', '>=', dateconv(self.arg['start']))
		if self.arg['end'] <> '':
			self.andwhere('timestamp', '<=', dateconv(self.arg['end']))
		self.end()
		return self.stmt
	
	#|'WHERE' and 'AND' commands used to build final statement string
	def where(self, name, sign, variable):
		self.stmt = self.stmt + ' WHERE %s %s "%s"' % (name, sign, variable)
		print self.stmt	
	def andwhere(self, name, sign, variable):
		self.stmt = self.stmt + ' AND %s %s "%s"' % (name, sign, variable)
	def end(self):
		self.stmt = self.stmt + ';'			

#|Convert datetime to timestamp
def dateconv(date):
	date = datetime.strptime(date, "%m/%d/%y")		
	timestamp = int(mktime(date.timetuple()))	
	return timestamp

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
		table = Table(table_name, meta, Column('timestamp', Integer),
			Column('price', Float), Column('amount', Float),
			Column('open', Float), Column('high', Float),
			Column('low', Float), Column('exchange', String(20)),
			Column('source', String(20)))	
	if create == 'yes':
		meta.create_all(eng)
	return table



