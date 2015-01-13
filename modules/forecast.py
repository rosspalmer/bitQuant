import db
import datetime as dt
import numpy as np
import pandas as pd
import sklearn
import ctrades

from pandas.io.data import DataReader
from sklearn.linear_model import LogisticRegression
from sklearn.lda import LDA
from sklearn.qda import QDA

def lag_tseries(ts, period=5):
	tlag = pd.DataFrame(index=ts.index)
	tlag['price'] = ts['price']
	tlag['amount'] = ts['amount']

	for i in xrange(0, period):
		tlag['lag%s' % str(i+1)] = ts['price'].shift(i+1)
		
	tret = pd.DataFrame(index=tlag.index)
	tret['price'] = tlag['price'].pct_change()*100.0
	tret['amount'] = tlag['amount']
	
	for i, x in enumerate(tret['price']):
		if (abs(x) < 0.0001):
			tret['price'][i] = 0.0001

	for i in xrange(0, period):
		tret['lag%s' % str(i+1)] = tlag['lag%s' % str(i+1)].pct_change()*100.0
		
	tret['dir'] = np.sign(tret['price'])
	
	return tret

def fit_model(name, model, x_train, y_train, x_test, pred):	       
        model.fit(x_train, y_train)	
        pred[name] = model.predict(x_test)
        pred['%s_Correct' % name] = (1.0+pred[name]*pred['Actual'])/2.0	
        hit_rate = np.mean(pred['%s_Correct' % name])
	print '%s: %.3f' % (name, hit_rate)

if __name__ == '__main__':
	
        period = 5
	table = db.tables('pricehis')
	trades = ctrades.trades()
        trades.add(table, 'bitfinex')
        trades.time_series(3600)
        btcret = lag_tseries(trades.ts, period)
        btcret = btcret[(period+2):]

	X = btcret[['lag1','lag2']]
	Y = btcret['dir']
	
        mid = dt.datetime(2014,4,1)

	x_train = X[X.index < mid]
	x_test = X[X.index >= mid]
	y_train = Y[Y.index < mid]
	y_test = Y[Y.index >= mid]
	
	pred = pd.DataFrame(index=y_test.index)
	pred['Actual'] = y_test

	print 'Hit Rates:'
	models = [('LR', LogisticRegression()), ('LDA', LDA()), ('QDA', QDA())]
        for m in models:
		fit_model(m[0], m[1], x_train, y_train, x_test, pred)
	
