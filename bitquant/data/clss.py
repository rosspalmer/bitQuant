import conv
import tools
from ..api.clss import api
from ..sql.clss import sql

from pandas import DataFrame
import time as tm

class data(object):

    def __init__(self):
        self.a = api()
        self.s = sql()
        self.jobs = []
        self.trd = DataFrame()
        self.prc = DataFrame()

    def add_trades(self, exchange, symbol, limit='', since='',
                    auto_since='no', ping_limit=1.0):
        job = {'exchange':exchange,'symbol':symbol}
        self.a.add_job(exchange, symbol, limit=limit, since=since,
                    auto_since=auto_since, ping_limit=ping_limit)
        self.jobs.append(job)

    def get_trades(self, exchange='', symbol='', start=''):
        trd = self.s.select('trades',exchange=exchange,
                    symbol=symbol,start=start)
        self.trd = self.trd.append(trd)
        self.trd = self.trd.drop_duplicates(['tid','exchange'])

    def run_trades(self, exchange, symbol):
        self.trd = self.trd.append(self.a.run(exchange,symbol))
        self.trd = self.trd.drop_duplicates(['tid','exchange'])

    def run_loop(self, time, to_sql=60):
        dump = tm.time() + to_sql
        end = tm.time() + time
        while tm.time() < end:
            for job in self.jobs:
                self.run_trades(job['exchange'], job['symbol'])
            if tm.time() > dump:
                dump = tm.time() + to_sql
                self.to_sql()

    def get_price(self, exchange='', symbol='',
                    freq='', start=''):
        prc = self.s.select('price',exchange=exchange,symbol=symbol,
                    freq=freq, start=start)
        self.prc = self.prc.append(prc)
        self.prc = self.prc.drop_duplicates(['timestamp','exchange',
                                        'symbol','freq'])
        return prc

    def run_price(self, exchange, symbol, freq, label='left',
                from_sql='no', start=''):
        if from_sql == 'yes':
            self.get_trades(exchange, symbol, start=start)
        trd = self.trd[(self.trd.exchange==exchange) \
                    & (self.trd.symbol==symbol)]
        trd = tools.date_index(trd)
        if len(trd.index) > 0:
            prc = conv.olhcv(trd, freq, label=label)
            self.prc = self.prc.append(prc)
            self.prc = self.prc.drop_duplicates(['timestamp','exchange',
                                        'symbol','freq'])

    def to_sql(self):
        if 'sent' in self.trd:
            trd = self.trd[self.trd['sent']<>'yes']
        else:
            trd = self.trd
        if 'sent'  in self.prc:
            prc = self.prc[self.prc['sent']<>'yes']
        else:
            prc = self.prc
        self.s.insert('trades', trd)
        self.s.insert('price', prc)
        print trd
        self.trd['sent'] = 'yes'
        self.prc['sent'] = 'yes'
