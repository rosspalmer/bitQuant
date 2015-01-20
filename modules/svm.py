import db

import numpy as np
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from sklearn import svm

def create_mach(sample, result, kernel='linear'):
	mach = svm.SVC(kernel)
	mach.fit(sample, result)
	return mach

def binary(df, column_name):
	df['binary'] = df[column_name].pct_change()
	df['binary'] = df['binary'].shift(-1)
	df['binary'] = df.apply(binaryfn, axis=1)
	return df

def binaryfn(row, limit= 0.007):
	if row['binary'] >= limit:
		result = 1
	elif row['binary'] <= -limit:
		result = -1
	else:
		result = 0
	return result

def split(ts, perc):
	inum = int(len(ts.index)*perc)
	index = ts['timestamp'].iloc[inum]
	ts1 = ts[ts['timestamp'] <= index]
	ts2 = ts[ts['timestamp'] > index]
	return ts1, ts2

def plot2D(df):
	df = df.drop('amount', axis=1)	
	df.plot()
	plt.show()

def prc_amt_lag(df, plags=1, alags=0):
	ts = DataFrame(index=df.index)
	ts['timestamp'] = df['timestamp']	
	ts['price'] = df['price']
	ts['amount'] = df['amount']
	ts['prc_change'] = df['price'].pct_change()*100.0
	ts['amt_change'] = df['amount'].pct_change()*100.0
	for i in range(1, plags + 1):
		header = 'pc_lag%s' % i
		ts[header] = ts['prc_change'].shift(i)
	for i in range(1, alags + 1):
		header = 'ac_lag%s' % i
		ts[header] = ts['amt_change'].shift(i)
	ts = ts[max(plags,alags)+1:]
	return ts

def zipcol(ts):
	print ts	
	c1 = ts['price']#.round(4).values
	c2 = ts['prc_change']#.round(4).values
	c3 = ts['pc_lag1']#.round(4).values
	c4 = ts['amount']#.round(4).values
	c5 = ts['amt_change']#.round(4).values	
	out = zip(c1, c2, c3, c4, c5)
	out = np.round(out, decimals=4)
	return out

def run():

	df = db.price_db('h', 'bitfinex', 'bcharttrades') #bcharttrades	
	ts = prc_amt_lag(df)
	ts = binary(ts, 'price')				
	#ts = ts.dropna()
	ts1, ts2 = split(ts, 0.50)
	sample = zipcol(ts1)	
	result = ts1['binary'].values	
	print result.sum()	
	mach = svm.SVC(kernel='linear')
	mach.fit(sample, result)
	print 'machine fit'
	test = zipcol(ts2)
	pred = mach.predict(test)
	pred = Series(pred, index=ts2.index, name='pred')
	ts2 = ts2.join(pred)
	summary = ts2[ts2['pred'] <> 0].drop(['amount','amt_change'], axis=1)	
	print summary

run()
