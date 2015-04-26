from ..data import tools

from sqlalchemy.sql import select

def auth():
    txt = open('auth_sql', 'r')
    typ = int(txt.readline().rstrip('\n'))
    if typ == 1:
        file_path = txt.readline().rstrip('\n')
        engine_str = 'sqlite+pysqlite:///%s' % file_path
    if typ == 2:
        host = txt.readline().rstrip('\n')
        user = txt.readline().rstrip('\n')
        password = txt.readline().rstrip('\n')
        name = txt.readline().rstrip('\n')
        engine_str = 'mysql+pymysql://%s:%s@%s/%s' % (user, password, host, name)
    return engine_str

def insert(tbl, sql_type):
    if sql_type == 'mysql':
        stmt = tbl.insert().prefix_with('IGNORE')
    if sql_type == 'sqlite':
        stmt = tbl.insert().prefix_with('OR IGNORE')
    return stmt

#|Currently broken
def select(tbl, exchange='',  symbol='', start='',
            end='', source='', freq=''):
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
        if source <> '':
            sel = sel.where(tbl.c.source == source)
        if freq <> '':
            sel = sel.where(tbl.c.freq == freq)
    return sel

