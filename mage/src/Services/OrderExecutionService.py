from mage.src.Services.Logger import Logger
from mage.src.Services.DTO.OpenPosition import OpenPosition
from mage.src.Services.DTO.ActionResult import ActionResult


class OrderExecutionService:

    def execute_buy(ts, portfolio, symbol, quantity, price):

        ## Update position - add
        if portfolio.has_open_long_position(symbol):
            position = portfolio.get_position(symbol)
            position.update_position(OpenPosition.POSITION_LONG, quantity, price)
            Logger.LOG("{} -- MARKET BUY add long position: symbol: {}, price: {}, quantity: {}".format(ts, symbol, position.cost_basis, position.quantity))
            return ActionResult.from_add_position(position.cost_basis, position.quantity, position.open_pnl) 
        
        ## Update position - close
        elif portfolio.has_open_short_position(symbol):
            position = portfolio.get_position(symbol)
            position.update_position(OpenPosition.POSITION_LONG, quantity, price)
            Logger.LOG("{} -- MARKET BUY close position: symbol: {}, price: {}, quantity: {}, pnl: {}".format(ts, symbol, position.cost_basis, position.quantity, position.final_pnl))
            if position.quantity == 0:        
                portfolio.remove_position(symbol)
            return ActionResult.from_close_position(position.cost_basis, position.quantity, position.open_pnl)

        ## Open new position
        else:
            position = OpenPosition.open_long(symbol, price, quantity)
            Logger.LOG("{} -- MARKET BUY open long position symbol: symbol: {}, price: {}, quantity: {}, size: {}".format(ts, symbol, position.cost_basis, position.quantity, position.position_size))
            portfolio.add_position(symbol, position)
            return ActionResult.from_open_position(position.cost_basis, position.quantity, position.open_pnl)
        

    def execute_sell(ts, portfolio, symbol, quantity, price):
        
        ## Update position - add
        if portfolio.has_open_short_position(symbol):
            position = portfolio.get_position(symbol)
            position.update_position(OpenPosition.POSITION_SHORT, quantity, price)
            Logger.LOG("{} -- MARKET SELL add short position: symbol: {}, price: {}, quantity: {}".format(ts, symbol, position.cost_basis, position.quantity))
            return ActionResult.from_add_position(position.cost_basis, position.quantity, position.open_pnl) 
        
        ## Update position - close
        elif portfolio.has_open_long_position(symbol):
            position = portfolio.get_position(symbol)
            position.update_position(price, quantity, price)
            Logger.LOG("{} -- MARKET SELL close position: symbol: {}, price: {}, quantity: {}, pnl: {}".format(ts, symbol, price, quantity, position.final_pnl))
            if position.quantity == 0:        
                portfolio.remove_position(symbol)
            return ActionResult.from_close_position(position.cost_basis, position.quantity, position.final_pnl)

        ## Open new position
        else:
            position = OpenPosition.open_short(symbol, price, quantity)
            Logger.LOG("{} -- MARKET SELL open short position symbol: {}, price: {}, quantity: {}".format(ts, symbol, position.cost_basis, position.quantity))
            portfolio.add_position(symbol, position)
            return ActionResult.from_open_position(position.cost_basis, position.quantity, position.open_pnl)
