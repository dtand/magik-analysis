from mage.src.Services.OrderExecutionService import OrderExecutionService
from mage.src.Services.Logger import Logger
from mage.src.Strategies.DTO.Variable import Variable

class LimitBuyOrder:
    
    def __init__(self, symbol, quantity, limit_price):
        self.order_type = "LIMIT_BUY"
        self.symbol = symbol
        self.quantity = quantity
        self.limit_price = limit_price

    def triggers(self, variable_table):
        return

class LimitSellOrder:
    
    def __init__(self, symbol, quantity, limit_price):
        self.order_type = "LIMIT_SELL"
        self.symbol = symbol
        self.quantity = quantity
        self.limit_price = limit_price

    def triggers(self, variable_table):
        return
    
class StopBuyOrder:
    
    def __init__(self, symbol, quantity, limit_price):
        self.order_type = "STOP_BUY"
        self.symbol = symbol
        self.quantity = quantity
        self.limit_price = limit_price

    def triggers(self, variable_table):
        return

class StopSellOrder:
    
    def __init__(self, symbol, quantity, limit_price):
        self.order_type = "STOP_SELL"
        self.symbol = symbol
        self.quantity = quantity
        self.limit_price = limit_price

    def triggers(self, variable_table):
        return
    
    
class BracketBuyOrder:

    def __init__(self, symbol, quantity, tp, sl):
        self.order_type = "BRACKET_BUY"
        self.symbol = symbol
        self.quantity = quantity
        self.tp = tp
        self.sl = sl
    
    def triggers(self, variable_table):
        return
    
class BracketSellOrder:

    def __init__(self, symbol, quantity, tp, sl):
        self.order_type = "BRACKET_SELL"
        self.symbol = symbol
        self.quantity = quantity
        self.tp = tp
        self.sl = sl

    def triggers(self, variable_table):
        return
    
class OrderBook:

    def __init__(self):
        self.open_orders = []

    def place_order(self, order):
        self.open_orders.append(order)

    def has_open_position(self, symbol):
        return symbol in self.open_orders
    
    def check_orders(self, variable_table, portfolio):
        action_results = []
        for order in self.open_orders:
            result, at_price = order.triggers(variable_table)
            if result:
                action_results.append((self.execute_order(order, at_price, variable_table, portfolio), order))
        return action_results
            
    def execute_order(self, order, at_price, variable_table, portfolio):
        ts = variable_table.get(Variable(symbol=order.symbol, var='timestamp'))
        Logger.LOG("{} -- {} triggered for symbol: {}".format(ts, order.order_type, order.symbol))
        if 'SELL' in order.order_type:
            return OrderExecutionService.execute_sell(ts, portfolio, order.symbol, order.quantity, at_price)
        else:
            return OrderExecutionService.execute_buy(ts, portfolio, order.symbol, order.quantity, at_price)




