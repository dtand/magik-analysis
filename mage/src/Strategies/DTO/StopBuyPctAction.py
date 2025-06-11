'''
    Action: Stop Buy Percent Action

    The stop buy action will place an order to buy an asset
    at a price above the the cost basis where the price is
    calculated as cost basis + percent_change(limit, cost basis)
'''

ACTION_NAME = "STOP_BUY_PCT"

class StopBuyPctAction:

    def __init__(self, limit=None):
        self.do = ACTION_NAME
        self.limit = limit

    def from_json(json_object):
        return StopBuyPctAction(json_object['limit'])
        