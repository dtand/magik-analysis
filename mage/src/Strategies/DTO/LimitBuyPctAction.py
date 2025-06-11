'''
    Action: Limit Buy Percent

    The limit buy percent action will place an order at limit x the current
    associated position's cost basis.  The limit value is expected to be a 
    percent.
'''

ACTION_NAME = "LIMIT_BUY_PCT"

class LimitBuyPctAction:

    def __init__(self, limit=None):
        self.do = ACTION_NAME
        self.limit = limit

    def from_json(json_object):
        return LimitBuyPctAction(json_object['limit'])
        