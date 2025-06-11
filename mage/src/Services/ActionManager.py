from mage.src.Strategies.DTO.ActionWrapper import VALID_ACTION_TYPES
from mage.src.Strategies.DTO.Variable import Variable
from mage.src.Services.DTO.OpenPosition import OpenPosition
from mage.src.Services.Logger import Logger
from mage.src.Services.OrderExecutionService import OrderExecutionService
from mage.src.Services.OrderBook import LimitBuyOrder
from mage.src.Services.OrderBook import LimitSellOrder
from mage.src.Services.OrderBook import StopBuyOrder
from mage.src.Services.OrderBook import StopSellOrder
from mage.src.Services.OrderBook import BracketBuyOrder
from mage.src.Services.OrderBook import BracketSellOrder
from mage.src.Services.DTO.ActionResult import ActionResult

class ActionManager:

    def perform_action(action, backtest_engine):

        action_type = action.action.do

        ## MARKET_BUY
        if action_type == VALID_ACTION_TYPES[0]:
            return ActionManager.do_market_buy(action, backtest_engine)

        ## MARKET_SELL
        elif action_type == VALID_ACTION_TYPES[1]:
            return ActionManager.do_market_sell(action, backtest_engine)

        ## LIMIT_BUY
        elif action_type == VALID_ACTION_TYPES[2]:
            return ActionManager.do_limit_buy(action, backtest_engine)

        ## LIMIT_SELL
        elif action_type == VALID_ACTION_TYPES[3]:
            return ActionManager.do_limit_sell(action, backtest_engine)

        ## STOP_BUY
        elif action_type == VALID_ACTION_TYPES[4]:
            return ActionManager.do_stop_buy(action, backtest_engine)

        ## STOP_SELL
        elif action_type == VALID_ACTION_TYPES[5]:
            return ActionManager.do_stop_sell(action, backtest_engine)

        ## BRACKET_BUY
        elif action_type == VALID_ACTION_TYPES[6]:
            return ActionManager.do_bracket_buy(action, backtest_engine)

        ## BRACKET_SELL
        elif action_type == VALID_ACTION_TYPES[7]:
            return ActionManager.do_bracket_sell(action, backtest_engine)

        ## LIMIT_BUY_PCT
        elif action_type == VALID_ACTION_TYPES[8]:
            return ActionManager.do_limit_buy_pct(action, backtest_engine)

        ## LIMIT_SELL_PCT
        elif action_type == VALID_ACTION_TYPES[9]:
            return ActionManager.do_limit_sell_pct(action, backtest_engine)

        ## BRACKET_BUY_PCT
        elif action_type == VALID_ACTION_TYPES[10]:
            return ActionManager.do_bracket_buy_pct(action, backtest_engine)

        ## BRACKET_SELL_PCT
        elif action_type == VALID_ACTION_TYPES[11]:
            return ActionManager.do_bracket_sell_pct(action, backtest_engine)

        ## STOP_BUY_PCT
        elif action_type == VALID_ACTION_TYPES[12]:
           return ActionManager.do_stop_buy_pct(action, backtest_engine)

        ## STOP_SELL_PCT
        elif action_type == VALID_ACTION_TYPES[13]:
            return ActionManager.do_stop_sell_pct(action, backtest_engine)

        ## SIGNAL_RESET
        elif action_type == VALID_ACTION_TYPES[14]:
            return ActionManager.do_signal_reset(action, backtest_engine)
        
        raise Exception("Invalid action type provided: {}, must be one of: {}".format(action_type, VALID_ACTION_TYPES))

    def do_market_buy(action, backtest_engine):
        portfolio = backtest_engine.portfolio
        ts = backtest_engine.variable_table.get(Variable(action.symbol, 'timestamp', 0))

        curr_market_value = backtest_engine.variable_table.get(Variable(action.symbol, 'open', 1))

        if curr_market_value == None:
            curr_market_value = backtest_engine.variable_table.get(Variable(action.symbol, 'close', 0))

        quantity = action.size.get_real_size(portfolio.get_position(action.symbol), backtest_engine.variable_table)
        return OrderExecutionService.execute_buy(ts, portfolio, action.symbol, quantity, curr_market_value)
    
    def do_market_sell(action, backtest_engine):
        portfolio = backtest_engine.portfolio
        ts = backtest_engine.variable_table.get(Variable(action.symbol, 'timestamp', 0))

        curr_market_value = backtest_engine.variable_table.get(Variable(action.symbol, 'open', 1))

        if curr_market_value == None:
            curr_market_value = backtest_engine.variable_table.get(Variable(action.symbol, 'close', 0))

        quantity = action.size.get_real_size(portfolio.get_position(action.symbol), backtest_engine.variable_table)
        return OrderExecutionService.execute_sell(ts, portfolio, action.symbol, quantity, curr_market_value)
    
    def do_limit_buy(action, backtest_engine):
        portfolio = backtest_engine.portfolio
        open_position = portfolio.get_open_position(action.symbol)
        quantity = action.size.get_real_size(open_position,backtest_engine.variable_table)
        
        order_book = backtest_engine.order_book
        order_book.place_order(LimitBuyOrder(action.symbol, quantity, action.action.limit))
        return ActionResult.from_place_order()
    
    def do_limit_sell(action, backtest_engine):
        portfolio = backtest_engine.portfolio
        open_position = portfolio.get_open_position(action.symbol)
        quantity = action.size.get_real_size(open_position,backtest_engine.variable_table)
    
        order_book = backtest_engine.order_book
        order_book.place_order(LimitSellOrder(action.action.symbol, quantity, action.action.limit))
        return ActionResult.from_place_order()

    def do_stop_buy(action, backtest_engine):
        portfolio = backtest_engine.portfolio
        open_position = portfolio.get_open_position(action.symbol)
        quantity = action.size.get_real_size(open_position,backtest_engine.variable_table)

        order_book = backtest_engine.order_book
        order_book.place_order(StopBuyOrder(action.action.symbol, quantity, action.action.limit))
        return ActionResult.from_place_order()
    
    def do_stop_sell(action, backtest_engine):
        portfolio = backtest_engine.portfolio
        open_position = portfolio.get_open_position(action.symbol)
        quantity = action.size.get_real_size(open_position,backtest_engine.variable_table)        
        
        order_book = backtest_engine.order_book
        order_book.place_order(StopSellOrder(action.action.symbol, quantity, action.action.limit))
        return ActionResult.from_place_order()

    def do_bracket_buy(action, backtest_engine):
        portfolio = backtest_engine.portfolio
        open_position = portfolio.get_open_position(action.symbol)
        quantity = action.size.get_real_size(open_position, backtest_engine.variable_table)

        order_book = backtest_engine.order_book
        order_book.place_order(BracketBuyOrder(action.action.symbol, quantity, action.action.take_profit, action.action.stop_loss))
        return ActionResult.from_place_order()
    
    def do_bracket_sell(action, backtest_engine):
        portfolio = backtest_engine.portfolio
        open_position = portfolio.get_open_position(action.symbol)
        quantity = action.size.get_real_size(open_position,backtest_engine.variable_table)

        order_book = backtest_engine.order_book
        order_book.place_order(BracketSellOrder(action.action.symbol, quantity, action.action.take_profit, action.action.stop_loss))
        return ActionResult.from_place_order()
    
    def do_limit_buy_pct(action, backtest_engine):
        action.action.limit = ActionManager.get_limit_from_percent(backtest_engine.portfolio.get_position(), action.action.limit)
        ActionManager.do_limit_buy(action, backtest_engine)
        return ActionResult.from_place_order()
    
    def do_limit_sell_pct(action, backtest_engine):
        action.action.limit = ActionManager.get_limit_from_percent(backtest_engine.portfolio.get_position(), action.action.limit)
        ActionManager.do_limit_sell(action, backtest_engine)
        return ActionResult.from_place_order()

    def do_stop_buy_pct(action, backtest_engine):
        action.action.limit = ActionManager.get_limit_from_percent(backtest_engine.portfolio.get_position(), action.action.limit)
        ActionManager.do_stop_buy(action)
        return ActionResult.from_place_order()
    
    def do_stop_sell_pct(action, backtest_engine):
        portfolio = backtest_engine.portfolio
        open_position = portfolio.get_open_position(action.symbol)
        quantity = action.size.get_real_size(open_position,backtest_engine.variable_table)

        action.action.limit = ActionManager.get_limit_from_percent(backtest_engine.portfolio.get_position(), action.action.limit)
        ActionManager.do_stop_sell(action, backtest_engine)
        return ActionResult.from_place_order()

    def do_bracket_buy_pct(action, backtest_engine):
        portfolio = backtest_engine.portfolio
        open_position = portfolio.get_open_position(action.symbol)
        quantity = action.size.get_real_size(open_position, backtest_engine.variable_table)

        action.action.take_profit = ActionManager.get_limit_from_percent(backtest_engine.portfolio.get_position(), action.action.take_profit)
        action.action.stop_loss = ActionManager.get_limit_from_percent(backtest_engine.portfolio.get_position(), action.action.stop_loss)
        ActionManager.do_bracket_buy(action, backtest_engine)
        return ActionResult.from_place_order()
    
    def do_bracket_sell_pct(action, backtest_engine):
        portfolio = backtest_engine.portfolio
        open_position = portfolio.get_open_position(action.symbol)
        quantity = action.size.get_real_size(open_position,backtest_engine.variable_table)

        action.action.take_profit = ActionManager.get_limit_from_percent(backtest_engine.portfolio.get_position(), action.action.take_profit)
        action.action.take_profit = ActionManager.get_limit_from_percent(backtest_engine.portfolio.get_position(), action.action.stop_loss)
        ActionManager.do_bracket_sell(action, backtest_engine)
        return ActionResult.from_place_order()
    
    def do_signal_reset(action, backtest_engine):
        backtest_engine.variable_table.set_global(action.action.signal, False)
        return ActionResult.from_misc()
    
    def get_limit_from_percent(position, percent):
        cost_basis = position.cost_basis
        return cost_basis + (percent * cost_basis)