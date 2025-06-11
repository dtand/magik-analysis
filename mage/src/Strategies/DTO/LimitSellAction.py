'''
    Action: Limit Sell

    The limit sell action will place an order at the designated limit value.
'''

ACTION_NAME = "LIMIT_SELL"

class LimitSellAction:

    def __init__(self, limit=None):
        self.do = ACTION_NAME
        self.limit = limit

    def from_json(json_object):
        return LimitSellAction(json_object['limit'])
        