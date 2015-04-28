import clss

def setup_sql():
    menu()
    s = clss.sql()
    s.meta.create_all(s.eng)

def menu():
    txt = open('auth_sql', 'w')
    print
    print '-----SQL Database setup-----'
    print
    print '=Select SQL type='
    print '  (1) sqlite'
    print '  (2) MySQL'
    print
    typ = int(raw_input(': '))
    print
    print
    if typ == 1:
        file_path = str(raw_input('Database Name: ')) + '\n'
        txt.write(str(typ) + '\n')
        txt.write(file_path)
    if typ == 2:
        host = str(raw_input('Host: ')) + '\n'
        user = raw_input('Username: ') + '\n'
        password = raw_input('Password: ') + '\n'
        name = raw_input('Database Name: ') + '\n'
        print
        txt.write(str(typ) + '\n')
        txt.write(host)
        txt.write(user)
        txt.write(password)
        txt.write(name)
