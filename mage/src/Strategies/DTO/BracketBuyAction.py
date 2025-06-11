'''
    Action: Bracket Buy

    The bracket buy action is a follow-up action to be used
    after opening a short position.  The action will trigger 
    either a limit buy at the take_profit, or a limit buy at
    the provided stop loss.
'''

ACTION_NAME = "BRACKET_BUY"

class BracketBuyAction:

    def __init__(self, take_profit, stop_loss):
        self.do = ACTION_NAME
        self.take_profit = take_profit
        self.stop_loss = stop_loss

    def from_json(json_object):
        return BracketBuyAction(json_object['take_profit'], json_object['stop_loss'])
