import db
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from sklearn import svm

def binary(df, column_name):
	df['binary'] = df[column_name].pct_change()
	df['binary'] = df['binary'].shift(-1)
	df['binary'] = df.apply(binaryfn, axis=1)
	return df

def binaryfn(row):
	rng = 0.007	
	if row['binary'] >= rng:
		result = 1
	elif row['binary'] <= -rng:
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

def prc_amt_lag(df, plags=3, alags=0):
	ts = DataFrame(index=df.index)
	ts['timestamp'] = df['timestamp']	
	ts['price'] = df['price']
	ts['amount'] = df['amount']
	for i in range(1, plags + 1):
		header = 'plag%s' % i
		ts[header] = df['price'].shift(i)
	for i in range(1, alags + 1):
		header = 'alag%s' % i
		ts[header] = df['amount'].shift(i)
	ts = ts[max(plags,alags):]
	return ts

def zipcol(ts)

def run():

	df = db.price_db('h', 'bitfinex', 'livetrades')
	ts = prc_amt_lag(df)
	ts = binary(ts, 'price')
	ts1, ts2 = split(ts, 0.75)
	#price = ts1['price'].values
	#amount = ts1['amount'].values
	#data = zip(price, amount)
	#print('zip')
	#result = ts1['binary'].values

	#mach = svm.SVC()
	#mach.fit(data, result)

	#price = ts2['price'].values
	#amount = ts2['amount'].values
	#pred = mach.predict(data)
	#data = zip(price, amount, pred)
	#df = DataFrame(data, index=ts2.index, columns=('price','amount','pred'))

run()
