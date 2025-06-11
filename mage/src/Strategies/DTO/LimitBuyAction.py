'''
    Action: Limit Buy

    The limit buy action will place an order at the designated limit value.
'''

ACTION_NAME = "LIMIT_BUY"

class LimitBuyAction:

    def __init__(self, limit):
        self.do = ACTION_NAME
        self.limit = limit

    def from_json(json_object):
        return LimitBuyAction(json_object['limit'])
        