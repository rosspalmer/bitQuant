import rest

import time as tm

#|API class is used to perform GET requests for
#|trades histories from exchange APIs
class api(object):

    def __init__(self):
        self.jobs = {}
        self.job = {}

    #|Add GET request job and set parameters for job
    def add_job(self, exchange, symbol, type, limit='',
                    since='', auto_since='no',ping_limit=1.0):

        #|Create 'job' dictionary
        job = {'exchange':exchange, 'symbol':symbol, 'type':type,
                    'limit':limit, 'market':'',
                    'since':since, 'auto_since':auto_since,
                    'ping_limit':ping_limit, 'next':0}

        #|Build statement for REST API request
        job['stmt'] = rest.build_stmt(job)

        #|Create nested dictionary if not present for exchange/symbol/type combo
        if not exchange in self.jobs.keys():
            self.jobs[exchange] = {}
        if not symbol in self.jobs[exchange].keys():
            self.jobs[exchange][symbol] = {}
        if not type in self.jobs[exchange][symbol].keys():
            self.jobs[exchange][symbol][type] = {}

        #|Add job to 'jobs' dictionary
        self.jobs[exchange][symbol][type] = job

    #|Run GET request job and return trade history DataFrame
    def run(self, exchange, symbol, type):

        #|Load job and run "limiter" function to pause in order not to exceed jobs per second rate
        self.load_job(exchange, symbol, type)
        self.limiter()

        #|Send GET API request and return DataFrame and updated 'job' dictionary
        df, self.job = rest.get(self.job)

        #|Run trade history jobs
        if self.job['type'] == 'trades':
            if self.job['auto_since'] == 'yes' \
                        and len(df.index) > 0:
                self.auto_since(df)
                self.job['stmt'] = rest.build_stmt(self.job)

        return df

    #|Update 'jobs' dictionary for previous job and load current 'job'
    def load_job(self, exchange, symbol, type):
        if not len(self.job) == 0:
            self.jobs[self.job['exchange']][self.job['symbol']][self.job['type']] \
                        = self.job
        self.job = self.jobs[exchange][symbol][type]

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

