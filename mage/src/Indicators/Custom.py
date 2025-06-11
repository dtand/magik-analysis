import numpy as np
from Utils import math_utils

class Custom:

    def REAL(closes, lows, highs):
        values = []
        for i in range(0, len(closes)):
            close = closes[i]
            low = lows[i]
            high = highs[i]
            values.append((close + low + high) / 3)
        return np.array(values)
    
    def DELTA(values, d1, d2):
        start = max(-1*d1, -1*d2)
        deltas = [np.nan] * start

        for i in range(start, len(values)):
            d1_val = values[i+d1]
            d2_val = values[i+d2]
            
            deltas.append(d1_val - d2_val)

        return np.array(deltas)
    
    def DELTA_PCT(values, d1, d2):
        start = max(-1*d1, -1*d2)
        deltas = [np.nan] * start

        for i in range(start, len(values)):
            d1_val = values[i+d1]
            d2_val = values[i+d2]
            
            deltas.append(math_utils.percentage_difference(d1_val, d2_val))

        return np.array(deltas)
    
    def VAR_CHANGE(values_x, values_y):
        change = []
        for i in range(0, len(values_x)):
            x = values_x[i]
            y = values_y[i]
            change.append(x-y)
        return np.array(change)
    
    def VAR_CHANGE_PTC(values_x, values_y):
        change = []
        for i in range(0, len(values_x)):
            x = values_x[i]
            y = values_y[i]
            change.append(math_utils.percentage_difference(x, y))
        return np.array(change)
    

