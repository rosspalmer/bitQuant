import api
import data
import tools

import pandas as pd
import time as tm

#|Cron class used for running cron scripts to
#|automatically update trade data and convert to price history
class cron(object):
	
	def __init__(self):
		self.pjob = []	
		self.tjob = []
	
	#|--------User functions--------------

	#|Add a trade job to 'tjob' list
	def add_tjob(self, exchange, symbol, limit=''): 
		job = {'exchange':exchange,'symbol':symbol,'limit':limit,
			'ratio':1}
		self.tjob.append(job)

	#|Add price job to 'pjob' list
	def add_pjob(self, exchange, symbol, freq):
		job = {'exchange':exchange,'symbol':symbol,'freq':freq,
			'start':0,'next':0}
		self.pjob.append(job)


	#|Loop through trade jobs and run if current loop count(i)
	#|is a multiple ratio value and run price job trigger function
	def run(self, time, mode='order', log='no'):
		end = tm.time() + time
		i = 1
		l = api.limiter()
		while tm.time() < end:
			for job in self.tjob:
				if i % job['ratio'] == 0:
					if log == 'yes':
						print job
					l.limit()					
					job = self.tjob_run(job)	
			if mode == 'ratio':			
				self.tjob_ratio()
			if len(self.pjob) > 0:
				self.pjob_trig(log)
			i += 1
				
	#|--------Trade job functions------------

	#|Set ratio variables for each trade job by reducing velocity ratio
	def tjob_ratio(self):		
		vels = []
		i = 0
		for job in self.tjob:
			try:			
				vels.append(job['vel'])
			except:
				pass
		vmax = max(vels)
		ratio = [int(round((1.0/vel)*vmax)) for vel in vels]
		for job in self.tjob:
			job['ratio'] = ratio[i]
			i += 1

	#|Ping API for trade data and add to SQL database
	#|Optional setting to return trade velocity in trades per hour
	def tjob_run(self, job):	
		ping = api.request(job['exchange'], job['symbol'], limit=job['limit'])
		try:
			trd = ping.to_sql()
		except:
			print 'Error: Did not connect to exchange API'
			return job
		num = float(len(trd.index))
		time = float(int(trd['timestamp'].max())-int(trd['timestamp'].min()))
		job['vel'] = int(round((num/time)*3600))
		return job

	#|------Price job functions--------

	#|Determine next timestamp 
	def pjob_next(self, job, prc):
		if len(prc.index) >= 2:		
			last = prc['timestamp'].max()
			period = prc['period'].min()
			job['next'] = last + 2*period
			job['start'] = last - period
		return job		

	#|Run trades to price conversion, add to SQL, and set 'next' and 'start' values
	def pjob_run(self, job):
		top = data.trades_to_price(job['exchange'], job['symbol'], job['freq'],
					start=job['start'], mode='period')
		top.to_sql()
		return self.pjob_next(job, top.prc)
		
	#|Cycle through jobs in 'pjob' list and trigger run function
	#|if 'next' value is less than current timestamp
	def pjob_trig(self, log):
		for job in self.pjob:
			if job['next'] < tm.time():
				if log == 'yes':
						print job
				job = self.pjob_run(job)
					
