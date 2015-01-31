class event(object):
	pass

class market_event(event):
	def __init__(self):
		self.type = 'market'

class signal_event(event):
	def __init__(self, symbol, datetime, signal_type):
		self.type = 'signal'
		self.symbol = symbol
		self.datetime = datetime
		self.signal_type = signal_type

class order_event(event):
	def __init__(self, symbol, order_type, quantity
		self.type = 'order'
		self.symbol = symbol
		self.order_type = order_type
		self.quantity = quantity
		self.direction = direction

	def print_order(self):
		print 'Order: symbol=%s, type=%s, quantity=%s, direction=%s' % \
			(self.symbol, self.type, self.quantity=%s, self.direction=%s)
		
def fill_event(event):
	def __init__(self, timeindex, symbol, exchange, quantity,
			direction, fill_cost):
		self.type = 'fill'
		self.timeindex = timeindex
		self.symbol = symbol
		self.exchange = exchange
		self.quantity = quantity
		self.direction = direction
		self.fill_cost = fill_cost
		self.commission = 0.0

