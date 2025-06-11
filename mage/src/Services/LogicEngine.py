import math

class LogicEngine:

    def assess_statement(criteria, variables):

        if criteria == None:
            return True
        
        var1 = LogicEngine.extract_var(criteria.var1, variables)
        var2 = LogicEngine.extract_var(criteria.var2, variables)

        if var1 is None or var2 is None or math.isnan(var1) or math.isnan(var2):
            return False
        
        result = LogicEngine.compare(var1, criteria.op, var2)

        for or_op in criteria.or_ops:
            result = result or LogicEngine.assess_statement(or_op, variables)

        for and_op in criteria.and_ops:
            result = result and LogicEngine.assess_statement(and_op, variables)

        return result
        
    def extract_var(var, variables):
        v = variables.get(var)
        if v is None:
            return None
        return float(v)
    
    def compare(var1, op, var2):
        match op:
            case "gt": return LogicEngine.gt(var1, var2)
            case "lt": return LogicEngine.lt(var1, var2)
            case "gteq": return LogicEngine.gteq(var1, var2)
            case "lteq": return LogicEngine.lteq(var1, var2)
            case "eq": return LogicEngine.eq(var1, var2)
            case "neq": return LogicEngine.neq(var1, var2)
            case _: raise Exception("Invalid logic operator provided: {}")


    def gt(var1, var2):
        return var1 > var2

    def lt(var1, var2):
        return var1 < var2

    def eq(var1, var2):
        return var1 == var2

    def lteq(var1, var2):
        return var1 <= var2

    def gteq(var1, var2):
        return var1 >= var2

    def neq(var1, var2):
        return var1 != var2

