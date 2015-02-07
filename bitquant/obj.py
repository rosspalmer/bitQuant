import sql

import pandas as pd
import numpy as np
import math
from scipy.spatial.distance import euclidean

#|Price object class used to manipulate customize price data
class price_object(object):

	#|Initiate object and pull in price data from SQL
	def __init__(self, exchange='', freq='',
			source='',columns=[]):
		self.df = sql.price_df(exchange, freq, source)
		if len(columns) > 0:
			drp = []
			for x in self.df.columns:
				if x not in columns:				
					drp.append(x)		
			self.df = self.df.drop(drp, axis=1)
	
	#|Return object DataFrame
	def df(self):
		return self.df
	
	#|Add a "lagging" value(s) for a column in object dataframe
	def add_lags(self, column_name, lags=1, size=1):
		for i in range(lags):
			lag_name = '%s lag%s' % (column_name, str(i+1))
			self.df[lag_name] = self.df[column_name].shift((i+1)*size)
		self.df = self.df.dropna()
	
	#|Add column to dataframe with distance from "test" vector
	def distance(self, vector):	
		added_columns = []		
		for col in vector.keys():
			col_name = '--%s' % col
			self.df[col_name] = vector[col]
			added_columns.append(col_name)
		self.df['distance'] = self.df.apply(dis_function, axis=1)
		self.df = self.df.drop(added_columns, axis=1)
				
#|Euclidean distance function for pandas			
def dis_function(row):
	v1, v2 = [], []	
	for col_name in row.keys():
		if col_name.find('--') == 0:			
			v1.append(row[col_name])
			v2.append(row[col_name[2:]])		
	dist = euclidean(v1, v2)
	return dist
	
