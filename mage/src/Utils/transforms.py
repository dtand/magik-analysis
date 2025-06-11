# def do_transform(transform):
import math
RSI_RANGE  = [58, 80]
CLOSE_TO_A_HIGH = [0, 0.008]

def size_for_rsi(size, rsi, a_high_a_close):
    rsi_normal = ((1/(RSI_RANGE[1] - RSI_RANGE[0])) * (RSI_RANGE[1] - rsi)) * 2.5
    close_to_high_normal = max(1, (a_high_a_close / CLOSE_TO_A_HIGH[1]) * 1.5)
    size = math.ceil(size * rsi_normal * close_to_high_normal)

    if size > 15:
        return 15
    if size < 5:
        return 1
    
    return size
    