'''
    Action: Stop Sell Percent Action

    The stop sell action will place an order to sell an asset
    at a price below the cost basis where the price is
    calculated as cost basis - percent_change(limit, cost basis)
'''

ACTION_NAME = "STOP_SELL_PCT"

class StopSellPctAction:

    def __init__(self, limit=None):
        self.do = ACTION_NAME
        self.limit = limit

    def from_json(json_object):
        return StopSellPctAction(json_object['limit'])
        