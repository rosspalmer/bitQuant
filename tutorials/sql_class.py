import bitquant as bq

#|Setup SQL server
bq.setup_sql()

#|Create API and SQL objects
a = bq.api()
s = bq.sql()

#|Request trade history to insert into SQL database
a.add_job('bitfinex','btcusd','trades', limit=5)
a.add_job('btcchina','btccny','trades', limit=5)
bf_trd = a.run('bitfinex','btcusd','trades')
bc_trd = a.run('btcchina','btccny','trades')

#|Review pulled data
print bf_trd
print bc_trd

#|Insert trade history into SQL database
s.insert('trades', bf_trd)
s.insert('trades', bc_trd)

#|Pull (select) all trade history data from database
trd = s.select('trades')
print trd

#|Pull only trade history from 'btcchina' exchange
trd = s.select('trades', exchange='btcchina')
print trd
