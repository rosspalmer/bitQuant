import db
from ctrades import trades
from pandas import Series, DataFrame
import matplotlib.pyplot as plt

from sklearn import svm

def binary(df, column_name):
	df['binary'] = df[column_name].pct_change()/abs(df[column_name].pct_change())
	return df

def split(ts, perc):
	inum = int(len(ts.index)*perc)
	index = ts['timestamp'].iloc[inum]
	ts1 = ts[ts['timestamp'] <= index]
	ts2 = ts[ts['timestamp'] > index]
	return ts1, ts2

trd = trades()
trd.add('trades', exchange='btcchina')
print 'Trades loaded'
trd.time_series(3600)
print 'Time series created'
ts = trd.ts
ts2, ts1 = split(ts, 0.25) 
ts1 = binary(ts1, 'price')
print('split')
price = ts1['price'].values
amount = ts1['amount'].values
data = zip(price, amount)
print('zip')
result = ts1['binary'].values

mach = svm.SVC()
mach.fit(data, result)

#price = ts2['price'].values
#amount = ts2['amount'].values
#data = zip(price, amount)

pred = mach.predict(data)
print 'pred'
data = zip(price, pred*1300)
df = DataFrame(data, index=ts1.index)
print df
#ts2['prediction'] = series
df.plot()
plt.show()
