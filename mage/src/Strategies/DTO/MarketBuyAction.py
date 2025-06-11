'''
    Action: Market Buy

    Executes a buy at the next open price, or current close if
    there is no next open.
'''

ACTION_NAME = "MARKET_BUY"

class MarketBuyAction:

    def __init__(self):
        self.do = ACTION_NAME

    def from_json(json_object=None):
        return MarketBuyAction()
        