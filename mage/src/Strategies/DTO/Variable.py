
class Variable:

    def __init__(self, symbol=None, var=None, offset=None):
        self.symbol = symbol
        self.var = var
        self.offset = offset

    def from_json(json_object):

        ## Optional: offset
        offset = 0
        if 'offset' in json_object:
            if not isinstance(json_object['offset'], int):
                raise Exception("Invalid offset provided {}, must be int type".format(json_object['offset']))
            offset = json_object['offset']
        
        return Variable(json_object['symbol'], json_object['var'], offset)
    
    def from_symbol_value(symbol, value):
        return Variable(symbol=symbol, var=value)
    
    def from_value(value):
        return Variable(var=value)