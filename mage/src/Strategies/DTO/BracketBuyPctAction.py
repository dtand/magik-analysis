'''
    Action: Bracket Buy Percent

    The bracket buy action is a follow-up action to be used
    after opening a short position.  The action will trigger 
    either a limit buy at the take_profit, or a limit buy at
    the provided stop loss.  The take profit and stop loss values
    are percentages which will be multiplied by the associated
    open position's cost basis.
'''

ACTION_NAME = "BRACKET_BUY_PCT"

class BracketBuyPctAction:

    def __init__(self, take_profit, stop_loss):
        self.do = ACTION_NAME
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def from_json(json_object):
        return BracketBuyPctAction(json_object['take_profit'], json_object['stop_loss'])
