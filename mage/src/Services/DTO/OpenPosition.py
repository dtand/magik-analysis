import math
from mage.src.Utils.futures_utils import find_size_for_contract

class OpenPosition:

    POSITION_LONG = 'LONG'
    POSITION_SHORT = 'SHORT'

    def open_long(symbol, cost_basis, quantity):
        return OpenPosition(symbol=symbol, position=OpenPosition.POSITION_LONG, cost_basis=cost_basis, quantity=quantity)
    
    def open_short(symbol, cost_basis, quantity):
        return OpenPosition(symbol=symbol, position=OpenPosition.POSITION_SHORT, cost_basis=cost_basis, quantity=quantity)
    
    def __init__(self, symbol=None, position=None, quantity=None, cost_basis=None, open_pnl=None):
        self.symbol = symbol
        self.position = position
        self.quantity = quantity
        self.cost_basis = cost_basis
        self.open_pnl = open_pnl
        self.final_pnl = 0
        self.cost_per_contract = find_size_for_contract(symbol)
        self.position_size = self.quantity * self.cost_basis * self.cost_per_contract

    def update_position(self, position, quantity, value):

        ## No position, opening new one
        if self.position == None:
            self.position = position
            self.quantity = quantity
            self.cost_basis = value

        ## Closing out some of the position
        elif self.position != position:
            self.update_final_pnl(quantity, value)
            self.update_cost_basis(quantity, value)
            self.quantity = self.quantity - quantity
            self.update_open_pnl(value)
            self.position_size = self.quantity * self.cost_basis * self.cost_per_contract

        ## Adding to existing position
        else:
            self.update_cost_basis(quantity, value)
            self.quantity = self.quantity + quantity
            self.update_open_pnl(value)           

    def close_position(self, value, size):
        quantity = math.floor(self.quantity * size)
        if quantity == self.quantity:
            self.position = None
            self.quantity = 0
            self.cost_basis = 0
            self.open_pnl = 0
        else:
            self.update_cost_basis(-1 * quantity, value)
            self.quantity = self.quantity - quantity
            self.update_open_pnl(value)

        return value * quantity

    def update_final_pnl(self, quantity, value):
        position_at_close = quantity * value * self.cost_per_contract
        pnl = position_at_close - self.position_size 
        if self.position == 'SHORT':
            pnl = pnl * -1
        self.final_pnl = pnl

    def update_cost_basis(self, quantity, value):
        cost_basis_new = quantity * value * self.cost_per_contract
        cost_basis_cur = self.quantity * self.cost_basis * self.cost_per_contract
        return (cost_basis_cur + cost_basis_new) / (self.quantity + quantity)

    def update_open_pnl(self, curr_asset_value):
        value_from_cost_basis = self.cost_basis * self.quantity * self.cost_per_contract
        value_from_curr_price = curr_asset_value * self.quantity * self.cost_per_contract
        
        if self.position == 'BUY' or self.position == 'LONG':
            self.open_pnl = (value_from_curr_price - value_from_cost_basis) / value_from_cost_basis
        elif self.position == 'SHORT':
            self.open_pnl = ((value_from_curr_price - value_from_cost_basis) / value_from_cost_basis) * -1