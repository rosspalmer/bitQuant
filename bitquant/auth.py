#|Load MySQL login information from text file in "auth" folder
#|Create login string for SQLAlchemy engine
def mysql(create='no'):
	if create == 'yes':
		mysql_create()
	txt = open('auth/mysql', 'r')
	host = txt.readline().rstrip('\n')
	user = txt.readline().rstrip('\n')
	password = txt.readline().rstrip('\n')
	engine_str = 'mysql+pymysql://%s:%s@%s/btc' % (user, password, host)
	return engine_str

#|Creates text file in "auth" folder which holds login for MySQL server
def mysql_create():
	print 'Please input MySQL login information'
	print
	host = str(raw_input('Host: ')) + '\n'
	user = raw_input('User: ') + '\n'
	password = raw_input('Password: ') + '\n'	
	txt = open('auth/mysql', 'w')
	txt.write(host)
	txt.write(user)
	txt.write(password)
