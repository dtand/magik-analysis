'''
    Action: Bracket Sell Percent

    The bracket sell action is a follow-up action to be used
    after opening a long position.  The action will trigger 
    either a limit sell at the take_profit, or a limit sell at
    the provided stop loss.
'''

ACTION_NAME = "BRACKET_SELL"

class BracketSellAction:

    def __init__(self, take_profit, stop_loss):
        self.do = ACTION_NAME
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def from_json(json_object):
        return BracketSellAction(json_object['take_profit'], json_object['stop_loss'])
        