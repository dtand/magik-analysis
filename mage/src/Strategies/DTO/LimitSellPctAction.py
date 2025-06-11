'''
    Action: Limit Sell

    The limit sell action will place an order at the designated limit value, such
    that the limit value is the percent change from the cost basis price.
'''

ACTION_NAME = "LIMIT_SELL"

class LimitSellPctAction:

    def __init__(self, limit=None):
        self.do = ACTION_NAME
        self.limit = limit

    def from_json(json_object):
        return LimitSellPctAction(json_object['limit'])
        