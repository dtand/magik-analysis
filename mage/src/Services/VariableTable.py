from mage.src.Strategies.DTO.Variable import Variable
import numbers
import datetime

class VariableTable:
    
    def __init__(self):
        self.data = {}
        self.epoch = 0
        self.globals = {}

    def get(self, var):
        symbol = var.symbol
        var_name = var.var
        offset = var.offset
        epoch = self.epoch
        if offset == None:
            offset = 0

        if symbol == None and not isinstance(var_name, numbers.Number):
            if var_name not in self.globals:
                return None
            else:
                return self.globals[var_name]
                    

        ## Hard coded numeric
        if isinstance(var_name, numbers.Number):
            return var_name
        
        ## Handle portfolio variables
        if 'position' in var.var:
            return self.handle_portfolio_var(var)
        
        ## Case where value is field inside another value, ie parent->child
        if '.' in var_name:
            parts = var_name.split('.')
            if parts[0] == 'timestamp':
                parent = self.data[symbol][parts[0]][epoch + offset]
                if epoch + offset >= len(self.data[symbol][parts[0]]):
                    return None
                return VariableTable.handle_datetime(parent, parts[1])
            else:
                child_data = self.data[symbol][parts[0]][parts[1]]
                if epoch + offset >= len(child_data):
                    return None
                return child_data[epoch + offset]
        
        ## Standard lookup
        else:
            if epoch + offset >= len(self.data[symbol][var_name]):
                return None
            return self.data[symbol][var_name][epoch + offset]

           
    def set_global(self, key, value):
        self.globals[key] = value 

    def handle_datetime(parent, field):
        if field == 'hour':
            return parent.hour
        return None
    
    def handle_portfolio_var(self, var):
        portfolio = self.globals['portfolio']
        open_position = portfolio.get_position(var.symbol)
        
        if open_position != None:
            if var.var == 'position':
                return True
            if var.var == 'position.position':
                return open_position.position
            elif var.var == 'position.cost_basis':
                return open_position.cost_basis
            elif var.var == 'position.quantity':
                return open_position.quantity
            elif var.var == 'position.open_pnl':
                return open_position.open_pnl
                
        return False

    def for_backtest(backtest_engine, symbols):
        variable_table = VariableTable()
        variable_table.data = backtest_engine.data
        return variable_table
    
    def for_analysis(analysis):
        variable_table = VariableTable()
        variable_table.data = analysis.data
        variable_table.epoch = analysis.curr_epoch
        return variable_table

    

