'''
    Action: Market Sell

    Executes a sell at the next open price, or current close if
    there is no next open.
'''

ACTION_NAME = "MARKET_SELL"

class MarketSellAction:

    def __init__(self):
        self.do = ACTION_NAME

    def from_json(json_object=None):
        return MarketSellAction()
        