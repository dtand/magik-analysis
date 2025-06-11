'''
    Action: Stop Buy Action

    The stop buy action will place an order to buy an asset
    at the specified price, given that the asset's price increases
    above the provided limit.
'''

ACTION_NAME = "STOP_BUY"

class StopBuyAction:

    def __init__(self, limit=None):
        self.do = ACTION_NAME
        self.limit = limit

    def from_json(json_object):
        return StopBuyAction(json_object['limit'])
        