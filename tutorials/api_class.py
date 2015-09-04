import bitquant as bq
import time as tm

#|Create API class
a = bq.api()

#|Add ticker request jobs
a.add_job('bitfinex','btcusd','ticker')
a.add_job('btce','ltcusd','ticker')
a.add_job('btcchina','btccny','ticker')

#|Add trade history request jobs
a.add_job('bitfinex','btcusd','trades')
a.add_job('coinbase','btcusd','trades')
a.add_job('btcchina','btccny','trades',limit=10)

#|Run ticker jobs and print returned DataFrames
print a.run('bitfinex','btcusd','ticker')
print a.run('btce','ltcusd','ticker')
print a.run('btcchina','btccny','ticker')

#|Run trades jobs and print returned DataFrames
print a.run('bitfinex','btcusd','trades')
print a.run('coinbase','btcusd','trades')
print a.run('btcchina','btccny','trades')

#|-----auto_since demonstration-------

a.add_job('okcoin','btccny','trades',auto_since='yes')

for i in range(10):
    print a.run('okcoin','btccny','trades')
