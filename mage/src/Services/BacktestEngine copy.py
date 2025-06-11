# from mage.src.Services.TradingReport import TradingReport
# from mage.src.Services.StrategyJsonParser import StrategyJsonParser
# from mage.src.Services.DataPrepService import DataPrepService
# from mage.src.Services.LogicEngine import LogicEngine
# from mage.src.Services.DTO.OpenPosition import OpenPosition
# from mage.src.Services.VariableTable import VariableTable
# from mage.src.Services.ActionManager import ActionManager
# from mage.src.Strategies.DTO.Variable import Variable
# from mage.src.Services.CSVService import CSVService
# from mage.src.Services.Logger import Logger
# from mage.src.Utils.futures_utils import find_size_for_contract
# from mage.src.Utils.data_utils import key_value_pairs_for_epoch
# from mage.src.Utils.transforms import size_for_rsi
# from mage.src.Services.DTO.Report import Report
# from mage.src.Services.OrderBook import OrderBook
# from mage.src.Services.Portfolio import Portfolio
# import math

# class BacktestEngine:


#     def __init__(self, capital=100000):
        
#         ## Required objects
#         self.portfolio = Portfolio()
#         self.order_book = OrderBook()
#         self.trading_report = TradingReport()
#         self.variable_table = None
        
#         ## Primitive members
#         self.strategy = None
#         self.data = None
#         self.symbols = []
#         self.capital = float(capital)
#         self.curr_epoch = 0
#         self.last_buy = 0
#         self.buys = 0
#         self.sells = 0
#         self.winners = []
#         self.losers = []
#         self.pnl = 0
#         self.sl = 0
#         self.orders = []
#         self.variable_table = None
#         self.report = Report()
#         self.size = 0
#         self.active_signals = set()
#         self.open_positions = {}

#     def init(self, symbols, strategy, data):
#         self.strategy = strategy
#         self.data = data
#         self.symbols = symbols
#         self.variable_table = VariableTable.for_backtest(self, symbols)

#     def prepare(self, strategy_json, symbols):
#         self.strategy = StrategyJsonParser.do_parse(strategy_json, symbols)
#         self.data = DataPrepService.get_data(self.strategy.data_specifications, symbols)
#         self.symbols = symbols
#         self.trading_report.set_time_period(self.data[symbols[0]]['timestamp'][0], self.data[symbols[0]]['timestamp'][-1])
#         self.variable_table = VariableTable.for_backtest(self, symbols)

#     def execute(self):
#         core_symbol = self.strategy.data_specifications[0].symbol
#         total_epochs = len(self.data[core_symbol]['open'])
#         for i in range(0, total_epochs):
#             self.curr_epoch = i
#             self.epoch()
#         return self.trading_report
    
#     def epoch(self):
#         self.update_variables()     ## Updates variable table with current state
#         self.handle_signals()       ## Checks to see if any signals are triggered
#         self.handle_orders()        ## Checks to see if any orders should be executed
#         self.handle_actions()       ## Performs any actions if criteria is met

#     def update_variables(self):
#         self.variable_table.epoch = self.curr_epoch
#         ts = self.data[self.symbols[0]]['timestamp'][self.curr_epoch]
#         if len(self.open_positions) > 0:
#             curr_close_price = self.data[self.symbols[0]]["close"][self.curr_epoch]
#             for key, value in self.open_positions.items():
#                 value.update_open_pnl(curr_close_price)
#                 self.open_positions[key] = value
#                 Logger.LOG("{} -- OPEN POSITION - SYMBOL: {}, QUANTITY: {}, POSITION: {}, PNL: {}%".format(ts, self.symbols[0], value.quantity, value.position, round(value.open_pnl*100, 2)))

#     def handle_signals(self):
#         ts = self.data[self.symbols[0]]['timestamp'][self.curr_epoch]
#         for signal in self.strategy.signals:
#             result = LogicEngine.assess_statement(signal.criteria, self.variable_table)
#             if result:
#                 if not self.variable_table.get(Variable(None, signal.identifier, 0)):
#                     Logger.LOG("{} -- ALERT SET {}".format(ts, signal.identifier))
#                     self.variable_table.set_global(signal.identifier, True)
#                     self.variable_table.set_global("{}_STATE".format(signal), self.curr_epoch)

#     def handle_orders(self):
#         self.order_book.check_orders()

#     def handle_actions(self):
#         self.check_orders()
#         actions_to_perform = self.assess_actions()
        
#         for action in actions_to_perform:
#             ActionManager.perform_action(action)

#     def add_order(self, action):
#         ts = self.data[action.symbol]['timestamp'][self.curr_epoch]
#         val = self.variable_table.get(action.at)
#         self.orders.append(action)
#         self.orders.append(action)
#         Logger.LOG("{} -- PLACE ORDER {} {} @ ${}".format(ts, action.do, action.size, val))

#     def assess_actions(self):
#         actions_to_perform = []
#         for action_with_criteria in self.strategy.actions:
#             result = LogicEngine.assess_statement(action_with_criteria.criteria, self.variable_table)
#             if result:
#                 actions_to_perform.append(action_with_criteria.action)
#                 for follow_up in action_with_criteria.follow_up_actions:
#                     actions_to_perform.append(follow_up)
#         return actions_to_perform
    
#     def check_orders(self):
#         orders_after = []
#         for order in self.orders:
#             # action = order[0]
#             # symbol = order[1]
#             # val = order[2]
#             # size = order[3]
#             # ## Stop loss sell triggers when period trades below trigger price
#             # if action == 'STOP_LOSS_SELL':
#             #     ts = self.data[symbol]['timestamp'][self.curr_epoch]
#             #     low = self.data[symbol]['low'][self.curr_epoch]
#             #     if low <= val:
#             #         Logger.LOG("{} -- STOP LOSS SELL at ${}".format(ts, val))
#             #         action = Action()
#             #         action.symbol = symbol
#             #         self.execute_sell(ts, action, val, self.size)
#             #     else:
#             #         orders_after.append(order)

#             if order.do == "STOP_LOSS_SELL_ORDER_PCT":
#                 symbol = order.symbol
#                 val = self.variable_table.get(order.at)

#                 if symbol in self.open_positions:
#                     entry = self.open_positions[symbol]
#                     stop_loss = entry.cost_basis - (val * entry.cost_basis)
#                     low = self.variable_table.get(Variable(symbol, 'low'))
#                     ts = self.variable_table.get(Variable(symbol, 'timestamp'))
#                     low = self.data[symbol]['low'][self.curr_epoch]
#                     if low <= stop_loss:
#                         Logger.LOG("{} -- STOP LOSS SELL at ${}".format(ts, stop_loss))
#                         action = Action()
#                         action.symbol = symbol
#                         self.execute_sell(ts, action, stop_loss, self.size)
#                         del self.open_positions[symbol]
#                     else:
#                         orders_after.append(order)

#         self.orders = orders_after

#     def do_buy2(self, action):
#         buy_at = self.data[action.symbol]['close'][self.curr_epoch]
#         if self.curr_epoch < len(self.data[action.symbol]['open']):
#             buy_at = self.data[action.symbol]['open'][self.curr_epoch+1]

#         low = self.data[action.symbol]['low'][self.curr_epoch]
#         ts = self.data[action.symbol]['timestamp'][self.curr_epoch]
#         #close_min_vwap = self.data[action.symbol]['close'][self.curr_epoch] - self.data[action.symbol]['VWAP_DELTA'][self.curr_epoch]


#         size = size_for_rsi(action.size, self.data[action.symbol]['RSI'][self.curr_epoch], self.data[action.symbol]['CTAH'][self.curr_epoch])

#         cost_per_contract = buy_at * find_size_for_contract(action.symbol)
#         cost_for_position = size * cost_per_contract
#         self.last_buy = cost_for_position
#         self.size = size

#         Logger.LOG("{} -- BUY {} contracts at ${}, position size: ${}".format(ts, size, open, cost_for_position))
#         self.buys = self.buys + 1
#         self.sl = low
#         entries = key_value_pairs_for_epoch(self.data[action.symbol], self.curr_epoch)
#         entries['Position Size'] = cost_for_position
#         self.report.add_entry(action, entries)

#         open_position = OpenPosition(action.symbol)
#         open_position.update_position("LONG", size, buy_at)
#         self.open_positions[action.symbol] = open_position
#         #self.open_positions["{}.open_pnl".format(action.symbol)] = open_position
#         #self.open_position = OpenPosition(action.symbol, cost_for_position, size, open, 0)


#     def do_sell2(self, action):

#         price = self.data[action.symbol]['close'][self.curr_epoch]
#         if self.curr_epoch+1 < len(self.data[action.symbol]['open']):
#             price = self.data[action.symbol]['open'][self.curr_epoch+1]
            
#         price = self.data[action.symbol]['open'][self.curr_epoch+1]

#         ## Execute at specified price
#         if action.at == 'MARKET_SELL':
#             price = action.at.var

#         ts = self.data[action.symbol]['timestamp'][self.curr_epoch]
#         size = action.size

#         self.execute_sell(ts, action, price, self.size)
#         del self.open_positions[action.symbol]

#         self.orders = []

#     def do_short_sell(self, action):  
#         short_at = self.data[action.symbol]['close'][self.curr_epoch]
        
#         if self.curr_epoch < len(self.data[action.symbol]['open']):
#             short_at = self.data[action.symbol]['open'][self.curr_epoch+1]

#         low = self.data[action.symbol]['low'][self.curr_epoch]
#         size = action.size
#         cost_per_contract = short_at * find_size_for_contract(action.symbol)
#         cost_for_position = size * cost_per_contract
#         self.last_buy = cost_for_position
#         self.size = size
#         ts = self.data[action.symbol]['timestamp'][self.curr_epoch]
#         Logger.LOG("{} -- SHORT SELL {} contracts at ${}, position size: ${}".format(ts, size, short_at, cost_for_position))
#         self.buys = self.buys + 1
#         self.sl = low
#         entries = key_value_pairs_for_epoch(self.data[action.symbol], self.curr_epoch)
#         entries['Position Size'] = cost_for_position
#         self.report.add_entry(action, entries)

#         open_position = OpenPosition(action.symbol)
#         open_position.update_position("SHORT", size, short_at)
#         self.open_positions[action.symbol] = open_position
#         #self.open_positions["{}.open_pnl".format(action.symbol)] = open_position
#         #self.open_position = OpenPosition(action.symbol, cost_for_position, size, open, 0)    

#     def do_buy_to_close(self, action):
#         price = self.data[action.symbol]['close'][self.curr_epoch]

#         if self.curr_epoch+1 < len(self.data[action.symbol]['open']):
#             price = self.data[action.symbol]['open'][self.curr_epoch+1]
            
#         price = self.data[action.symbol]['open'][self.curr_epoch+1]

#         ts = self.data[action.symbol]['timestamp'][self.curr_epoch]

#         self.execute_sell(ts, action, price, self.size)
#         del self.open_positions[action.symbol]

#         self.orders = []

#     def execute_sell(self, ts, action, price, size):


#         ## Closing a short
#         if action.do == 'BUY_TO_CLOSE':
#             cost_per_contract = price * find_size_for_contract(action.symbol)
#             cost_for_position = size * cost_per_contract
#             pnl = self.last_buy - cost_for_position

#             Logger.LOG("{} -- BUY TO CLOSE {} contracts at ${}, position size: ${}, profit: ${}".format(ts, size, price, cost_for_position, pnl))
            
#             self.last_buy = 0
#             self.sells = self.sells + 1
#             self.pnl = self.pnl + pnl
#             if pnl > 0:
#                 self.winners.append(pnl)
#             else:
#                 self.losers.append(pnl)
#             entries = key_value_pairs_for_epoch(self.data[action.symbol], self.curr_epoch)
#             entries['Position Size'] = cost_for_position
#             entries['PNL'] = pnl
#             self.report.add_entry(action, entries)

#         ## Closing a long
#         else:
#             cost_per_contract = price * find_size_for_contract(action.symbol)
#             cost_for_position = size * cost_per_contract
#             pnl = cost_for_position - self.last_buy
#             Logger.LOG("{} -- SELL {} contracts at ${}, position size: ${}, profit: ${}".format(ts, size, price, cost_for_position, pnl))
#             self.last_buy = 0
#             self.sells = self.sells + 1
#             self.pnl = self.pnl + pnl
#             if pnl > 0:
#                 self.winners.append(pnl)
#             else:
#                 self.losers.append(pnl)
#             entries = key_value_pairs_for_epoch(self.data[action.symbol], self.curr_epoch)
#             entries['Position Size'] = cost_for_position
#             entries['PNL'] = pnl
#             self.report.add_entry(action, entries)
        

#     def do_buy(self, action):
#         capital = self.capital * action.size
#         total_shares = 0
#         buy_at_price = 0
        
#         if capital <= 0:
#             return

#         if action.when == 'OPEN':
#             buy_at_price = self.data[action.symbol]['open'][self.curr_epoch+1]
#         elif action.when == 'CLOSE':
#             buy_at_price = self.data[action.symbol]['close'][self.curr_epoch]
#         else:
#             raise Exception("Invalid action.when provided: {}".format(action.when))
        
#         total_shares = math.floor(capital / buy_at_price)
#         self.capital = self.capital - capital

#         if self.open_position == None:
#             self.open_position = OpenPosition(action.symbol)
        
#         self.open_position.update_position("BUY", total_shares, buy_at_price)
#         Logger.LOG("BUY ACTION -- Purchasing asset: {} {} shares @ ${} on {}".format(total_shares, action.symbol, buy_at_price, self.data[action.symbol]['timestamp'][self.curr_epoch]))

#     def do_sell(self, action):
#         Logger.LOG("SELL ACTION -- Selling asset: {} {} shares @ ${} on {}".format(self.open_position.quantity, action.symbol, self.data[action.symbol]['close'][self.curr_epoch], self.data[action.symbol]['timestamp'][self.curr_epoch]))
#         capital_returned = self.open_position.close_position(self.data[action.symbol]['close'][self.curr_epoch], action.size)
#         self.capital = self.capital + capital_returned
#         self.open_position = None
#         self.trading_report.update_performance_metrics(self.capital)

#     def clear_signal(self, action):
#         ts = self.data[self.symbols[0]]['timestamp'][self.curr_epoch]
#         Logger.LOG("{} -- CLEAR SIGNAL {} ".format(ts, action.at.var))
#         var = action.at.var
#         self.variable_table.set_global(var, False)

#     def write_report(self):
#         csv_service = CSVService.from_report(self.report, self.strategy.name)
#         csv_service.write_to_folder('./Strategies/results')


