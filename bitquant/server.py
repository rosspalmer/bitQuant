import api
import data

import pandas as pd
import time as tm

#|Cron class used for running cron scripts to
#|automatically update trade data and convert to price history
class cron(object):
	
	def __init__(self):
		self.schedule = pd.DataFrame(columns=('exchange','symbol','job','limit',
					'since','freq','hard_time','start','next'))
		self.job = {}

	#|Add a trade "ping" job or convert trade to price
	def add_job(self, exchange, symbol, job, limit='', since='',
			freq='', hard_time=''):
		self.job = {'exchange':exchange,'symbol':symbol,'job':job,'limit':limit,'since':since, 
			'freq':freq,'hard_time':hard_time,'start':0,'next':0,'period':0}
		self.schedule = self.schedule.append(self.job, ignore_index=True)

	#|Update 'job' dictionary with next item on schedule
	def next_job(self):
		self.schedule = self.schedule.sort('next')
		self.job = self.schedule.iloc[0].to_dict()	

	#|Run cron job for set length (in seconds)
	def run(self, length):
		stop = tm.time() + length
		while tm.time()	<= stop:
			self.sleep()
			self.update()	

	#|Set 'next' timestamp for next trade "ping" job based on 'hard_time'
	def schedule_trades(self):
		self.job['next'] = int(tm.time() + self.job['hard_time'])

	#|Set 'next' for next trade to price conversion
	#|If 'hard_time' is not set then set time for next avaiable full bar
	def schedule_price(self, prc):
		self.job['start'] = int(prc['timestamp'].max())
		if self.job['period'] == 0:
			self.job['period'] = abs(prc['timestamp'].iloc[1]-prc['timestamp'].iloc[0])				
		if self.job['hard_time'] <> '':
			self.job['next'] = int(tm.time() + self.job['hard_time'])
		else:
			self.job['next'] = int(self.job['start'] + 2*self.job['period'] + 5)

	#|Sleep until next item on schedule
	def sleep(self):
		self.next_job()
		next = self.job['next']
		hold = int(next - tm.time())	
		if hold >= 3:
			tm.sleep(hold)

	#|Update trade data or conversion to price and add new job to schedule
	def update(self):
		self.next_job()
		if self.job['job'] == 'trades':
			self.update_trades()
		elif self.job['job'] == 'price':
			self.update_price()
		self.schedule = self.schedule[1:]
		self.schedule = self.schedule.append(self.job, ignore_index=True)

	#|Ping exchange API and add data to MySQL server
	def update_trades(self):
		ping = api.trades_api(self.job['exchange'], self.job['symbol'], 
				limit=self.job['limit'],since=self.job['since'])
		trd = ping.to_sql()
		self.schedule_trades()

	#|Convert trade data to price history
	def update_price(self):
		top = data.trades_to_price(self.job['exchange'], self.job['symbol'],
				self.job['freq'], int(self.job['start']))
		top.to_sql()
		if len(top.prc.index) > 0:
			self.schedule_price(top.prc)
		else:
			self.job['next'] = self.job['next'] + 20

