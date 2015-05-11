import stmt
from ..data.tools import date_index

from pandas import DataFrame
from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String, Float
from sqlalchemy.sql import select

class sql(object):

    def __init__(self):
        engine_str = stmt.auth()
        if engine_str.find('sqlite') == 0:
            self.sql_type = 'sqlite'
            self.eng = create_engine(engine_str, module=sqlite)
        else:
            self.sql_type = 'mysql'
            self.eng = create_engine(engine_str)
        self.conn = self.eng.connect()
        self.meta = MetaData(self.eng)
        self.tbl = self.load_tables()

    def insert(self, table_name, df):
        if len(df.index) > 0:
            data = df.to_dict('records')
            statement = stmt.insert(self.tbl[table_name], self.sql_type)
            statement.execute(data)

    def select(self, table_name, exchange='',  symbol='',
                start='', end='', source='', freq=''):
        tbl = self.tbl[table_name]
        #tbl = dic[table_name]
        #statement = stmt.select(tbl, exchange='',
            #symbol='', start='', end='', source='', freq='')
        sel = select([tbl])
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
        if freq <> '':
            sel = sel.where(tbl.c.freq == freq)
        result = self.conn.execute(sel)
        headers = result.keys()
        result = result.fetchall()
        df = DataFrame(result, columns=headers)
        return df

    def load_tables(self):

        tables = {}

        tables['trades'] = Table('trades', self.meta,
            Column('tid', Integer, primary_key=True),
            Column('price', Float), Column('amount', Float),
            Column('type', String(4)), Column('timestamp', Integer),
            Column('timestamp_ms', Integer),
            Column('exchange', String(20), primary_key=True),
            Column('symbol', String(6), primary_key=True))

        tables['price'] = Table('price', self.meta,
            Column('timestamp', Integer, primary_key=True),
            Column('exchange', String(20), primary_key=True),
            Column('symbol', String(6), primary_key=True),
            Column('freq', String(5), primary_key=True),
            Column('open', Float), Column('low', Float),
            Column('high', Float), Column('close', Float),
            Column('volume', Float), Column('vwap', Float))

        return tables
