import rest

import time as tm

#|API class is used to perform GET requests for
#|trades histories from exchange APIs
class api(object):

    def __init__(self):
        self.jobs = {}
        self.job = {}

    #|Add GET request job and set parameters for job
    def add_job(self, exchange, symbol, limit='',
                    since='', auto_since='no',ping_limit=1.0):
        job = {'exchange':exchange, 'symbol':symbol,
                    'limit':limit, 'market':'',
                    'since':since, 'auto_since':auto_since,
                    'ping_limit':ping_limit, 'next':0}
        stmt = rest.build_stmt(job)
        job['stmt'] = stmt
        if not exchange in self.jobs.keys():
            self.jobs[exchange] = {}
        self.jobs[exchange][symbol] = job

    #|Run GET request job and return trade history DataFrame
    def run(self, exchange, symbol):
        self.load_job(exchange, symbol)
        self.limiter()
        trd, self.job = rest.get(self.job)
        if self.job['auto_since'] == 'yes' \
                    and len(trd.index) > 0:
            self.auto_since(trd)
            self.job['stmt'] = rest.build_stmt(self.job)
        return trd

    #|Update 'job' dictionary for previous job and load current 'job'
    def load_job(self, exchange, symbol):
        if not len(self.job) == 0:
            self.jobs[self.job['exchange']][self.job['symbol']] \
                        = self.job
        self.job = self.jobs[exchange][symbol]

    #|Limit number of requests per sec
    def limiter(self):
        if tm.time() < self.job['next']:
            tm.sleep(self.job['next']-tm.time())

    #|Set 'since' variable in job to last tid/timestamp
    def auto_since(self, trd):
        cmd = rest.commands()[self.job['exchange']][self.job['symbol']]
        if 'stype' in cmd.keys():
            if cmd['stype'] == 'id':
                self.job['since'] = int(trd['tid'].max())
            if cmd['stype'] == 'timestamp':
                self.job['since'] = int(trd['timestamp'].max()) - 1