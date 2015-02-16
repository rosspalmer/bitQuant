import api
import sql

import pandas as pd
import time as tm

class cron(object):
	
	def __init__(self):
		self.schedule = pd.DataFrame(columns=('exchange','symbol','job'
					'parameter','start','next','factor'))
		self.job = {}

	def add_job(self, exchange, symbol, job, limit, freq='',factor=1.0):
		self.job = {'exchange':exchange, 'symbol':symbol, 
			'job':job, 'next':0, 'factor':factor}
		if job == 'price':
			self.job['start'] = 0
		self.schedule = self.schedule.append(self.job, ignore_index=True)

	def next_job(self):
		self.schedule = self.schedule.sort('next')
		self.job = self.schedule.iloc[0].to_dict()	

	def schedule_trades(self, trd):
		span = int(trd.iloc[0]['timestamp']) - int(trd.iloc[19]['timestamp'])
		vel = int(span/20)
		add = round(vel*self.job['parameter']/self.job['factor'],1)
		self.job['next'] = int(trd.iloc[0]['timestamp']) + add

	def schedule_price(self, prc):
		period = abs(prc['timestamp'].iloc[1]-prc['timestamp'].iloc[0])
		self.job['next'] = int(prc['timestamp'].iloc[-1] + period*self.job['factor'])
		self.job['start'] = int(prc['timestamp'].iloc[-2])

	def sleep(self):
		self.next_job()
		next = self.job['next']
		hold = int(next - tm.time())
		if hold >= 5:
			tm.sleep(hold)

	def update(self):
		self.next_job()
		if self.job['job'] == 'trades':
			self.update_trades()
		elif self.job['job'] == 'price':
			self.update_price()
		self.schedule = self.schedule[1:]
		self.schedule = self.schedule.append(self.job, ignore_index=True)

	def update_trades(self):
		ping = api.trades_api(self.job['exchange'], self.job['symbol'], 
				limit=self.job['parameter'])
		trd = ping.to_sql()
		self.schedule_trades(trd)

	def update_price(self):
		top = sql.trades_to_price(self.job['exchange'], self.job['symbol'],
				self.job['freq'], self.job['start'])
		prc = top.run()
		self.schedule_price(prc)


