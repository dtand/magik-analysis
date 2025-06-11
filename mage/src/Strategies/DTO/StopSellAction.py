'''
    Action: Stop Sell Action

    The stop sell action will place an order to sell an asset
    at the specified price, given that the asset's price drops
    below the provided limit.
'''

ACTION_NAME = "STOP_SELL"

class StopSellAction:

    def __init__(self, limit=None):
        self.do = ACTION_NAME
        self.limit = limit

    def from_json(json_object):
        return StopSellAction(json_object['limit'])
        