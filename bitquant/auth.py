#|Load MySQL login information from text file in "auth" folder
#|Create login string for SQLAlchemy engine
def sql():
	txt = open('auth_sql', 'r')
	typ = int(txt.readline().rstrip('\n'))
	if typ == 1:
		file_path = txt.readline().rstrip('\n')
		engine_str = 'sqlite+pysqlite:///%s' % file_path
	if typ == 2:	
		host = txt.readline().rstrip('\n')
		user = txt.readline().rstrip('\n')
		password = txt.readline().rstrip('\n')
		name = txt.readline().rstrip('\n')
		engine_str = 'mysql+pymysql://%s:%s@%s/%s' % (user, password, host, name)
	return engine_str

#|Creates text file in "auth" folder which holds login for MySQL server
def sql_setup():
	txt = open('auth_sql', 'w')	
	print
	print '-----SQL Database setup-----'
	print
	print 'Select SQL type'
	print '(1) sqlite'
	print '(2) MySQL'
	typ = int(raw_input(': '))
	print
	if typ == 1:
		file_path = str(raw_input('Filepath: ')) + '\n'
		txt.write(str(typ) + '\n')
		txt.write(file_path)
	if typ == 2:	
		host = str(raw_input('Host: ')) + '\n'
		user = raw_input('Username: ') + '\n'
		password = raw_input('Password: ') + '\n'
		name = raw_input('Database Name: ') + '\n'	
		txt.write(str(typ) + '\n')
		txt.write(host)
		txt.write(user)
		txt.write(password)
		txt.write(name)

