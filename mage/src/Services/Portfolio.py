from mage.src.Services.DTO.OpenPosition import OpenPosition
from mage.src.Strategies.DTO.Variable import Variable
class Portfolio:

    def __init__(self):
        self.open_positions = {}

    def add_position(self, symbol, position):
        self.open_positions[symbol] = position

    def update(self, variable_table):
        for key,value in self.open_positions.items():
            close = variable_table.get(Variable(symbol=key, var='close'))
            value.update_open_pnl(close)
            self.open_positions[key] = value

    def get_position(self, symbol):
        if not self.has_open_position(symbol):
            return None
        return self.open_positions[symbol]
    
    def has_open_position(self, symbol):
        return symbol in self.open_positions
    
    def has_open_long_position(self, symbol):
        return symbol in self.open_positions and self.open_positions[symbol].position == OpenPosition.POSITION_LONG
    
    def has_open_short_position(self, symbol):
        return symbol in self.open_positions and self.open_positions[symbol].position == OpenPosition.POSITION_SHORT
    
    def remove_position(self, symbol):
        del self.open_positions[symbol]