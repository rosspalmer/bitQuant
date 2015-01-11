# Input Login information
host = 'HOST'
user = 'USERNAME'
password = 'PASSWORD'

def mysql():
	engine_str = 'mysql+pymysql://%s:%s@%s/btc' % (user, password, host)
	return engine_str
