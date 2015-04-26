import rest

import time as tm

class api(object):

    def __init__(self):
        self.jobs = {}
        self.job = {}

    def add_job(self, exchange, symbol, mode='trades',
                    limit='', since='', auto_since='no',
                    ping_limit=1.0):
        job = {'exchange':exchange, 'symbol':symbol,
                    'mode':mode, 'limit':limit, 'market':'',
                    'since':since, 'auto_since':auto_since,
                    'ping_limit':ping_limit, 'next':0}
        stmt = rest.build_stmt(job)
        job['stmt'] = stmt
        if not exchange in self.jobs.keys():
            self.jobs[exchange] = {}
        self.jobs[exchange][symbol] = job

    def run(self, exchange, symbol):
        self.load_job(exchange, symbol)
        self.limiter()
        trd, self.job = rest.get(self.job)
        #if self.job['auto_since'] == 'yes':
        #    self.auto_since(trd)
        return trd

    def load_job(self, exchange, symbol):
        if not len(self.job) == 0:
            self.jobs[self.job['exchange']][self.job['symbol']] \
                        = self.job
        self.job = self.jobs[exchange][symbol]

    def limiter(self):
        if tm.time() < self.job['next']:
            tm.sleep(self.job['next']-tm.time())

    #|Currently broken
    def auto_since(self, trd):
        cmd = rest.commands()[self.job['exchange']][self.job['symbol']]
        if 'stype' in cmd.keys():
            if cmd['stype'] == 'id':
                self.job['since'] = int(trd['tid'].max())
            if cmd['stype'] == 'timestamp':
                self.job['since'] = int(trd['timestamp'].max()) - 1