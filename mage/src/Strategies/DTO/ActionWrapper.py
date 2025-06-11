from mage.src.Strategies.DTO.MarketBuyAction import MarketBuyAction
from mage.src.Strategies.DTO.MarketSellAction import MarketSellAction
from mage.src.Strategies.DTO.LimitBuyAction import LimitBuyAction
from mage.src.Strategies.DTO.LimitSellAction import LimitSellAction
from mage.src.Strategies.DTO.StopBuyAction import StopBuyAction
from mage.src.Strategies.DTO.StopSellAction import StopSellAction
from mage.src.Strategies.DTO.BracketBuyAction import BracketBuyAction
from mage.src.Strategies.DTO.BracketSellAction import BracketSellAction
from mage.src.Strategies.DTO.LimitBuyPctAction import LimitBuyPctAction
from mage.src.Strategies.DTO.LimitSellPctAction import LimitSellPctAction
from mage.src.Strategies.DTO.BracketBuyPctAction import BracketBuyPctAction
from mage.src.Strategies.DTO.BracketSellPctAction import BracketSellPctAction
from mage.src.Strategies.DTO.StopBuyPctAction import StopBuyPctAction
from mage.src.Strategies.DTO.StopSellPctAction import StopSellPctAction
from mage.src.Strategies.DTO.SignalResetAction import SignalResetAction
from mage.src.Strategies.DTO.OrderSize import OrderSize
from mage.src.Strategies.DTO.Criteria import Criteria

VALID_ACTION_TYPES = [  ## SIZE = 14
    'MARKET_BUY', 
    'MARKET_SELL', 
    'LIMIT_BUY', 
    'LIMIT_SELL', 
    'STOP_BUY',
    'STOP_SELL',
    'BRACKET_BUY', 
    'BRACKET_SELL',
    'LIMIT_BUY_PCT', 
    'LIMIT_SELL_PCT',
    'BRACKET_BUY_PCT', 
    'BRACKET_SELL_PCT',
    'STOP_BUY_PCT', 
    'STOP_SELL_PCT',
    'SIGNAL_RESET'
]

class ActionWrapper:

    def __init__(self, action=None, size=None, criteria=None, symbol=None, follow_up_actions=[]):
        self.action = action
        self.size = size
        self.criteria = criteria
        self.symbol = symbol
        self.follow_up_actions = follow_up_actions
        
    def from_json(json_object):
        action_type = json_object['action']['do']
        action = None 

        
        if action_type not in VALID_ACTION_TYPES:
            raise Exception("Invalid do provided: {}, must be one of: {}".format(action_type, VALID_ACTION_TYPES))
        
        ## MARKET_BUY
        if action_type == VALID_ACTION_TYPES[0]:
            action = MarketBuyAction.from_json()

        ## MARKET_SELL
        elif action_type == VALID_ACTION_TYPES[1]:
            action = MarketSellAction.from_json()

        ## LIMIT_BUY
        elif action_type == VALID_ACTION_TYPES[2]:
            action = LimitBuyAction.from_json(json_object['action'])

        ## LIMIT_SELL
        elif action_type == VALID_ACTION_TYPES[3]:
            action = LimitSellAction.from_json(json_object['action'])

        ## STOP_BUY
        elif action_type == VALID_ACTION_TYPES[4]:
            action = StopBuyAction.from_json(json_object['action'])

        ## STOP_SELL
        elif action_type == VALID_ACTION_TYPES[5]:
            action = StopSellAction.from_json(json_object['action'])

        ## BRACKET_BUY
        elif action_type == VALID_ACTION_TYPES[6]:
            action = BracketBuyAction.from_json(json_object['action'])

        ## BRACKET_SELL
        elif action_type == VALID_ACTION_TYPES[7]:
            action = BracketSellAction.from_json(json_object['action'])

        ## LIMIT_BUY_PCT
        elif action_type == VALID_ACTION_TYPES[8]:
            action = LimitBuyPctAction.from_json(json_object['action'])

        ## LIMIT_SELL_PCT
        elif action_type == VALID_ACTION_TYPES[9]:
            action = LimitSellPctAction.from_json(json_object['action'])

        ## BRACKET_BUY_PCT
        elif action_type == VALID_ACTION_TYPES[10]:
            action = BracketBuyPctAction.from_json(json_object['action'])

        ## BRACKET_SELL_PCT
        elif action_type == VALID_ACTION_TYPES[11]:
            action = BracketSellPctAction.from_json(json_object['action'])

        ## STOP_BUY_PCT
        elif action_type == VALID_ACTION_TYPES[12]:
            action = StopBuyPctAction.from_json(json_object['action'])

        ## STOP_SELL_PCT
        elif action_type == VALID_ACTION_TYPES[13]:
            action = StopSellPctAction.from_json(json_object['action'])

        ## SIGNAL_RESET
        elif action_type == VALID_ACTION_TYPES[14]:
            action = SignalResetAction.from_json(json_object['action'])


        ## Optional: 'size'
        size = None
        if 'size' in json_object:
            size = OrderSize.from_json(json_object['size'])
        
        ## Optional: 'criteria'
        criteria = None
        if 'criteria' in json_object:
            criteria = Criteria.from_json(json_object['criteria'])

        ## Optional: 'symbol'
        symbol = None
        if 'symbol' in json_object:
            symbol = json_object['symbol']

        ## Optional: followUpActions
        follow_up_actions = []
        if 'followUpActions' in json_object:
            for follow_up in json_object['followUpActions']:
                follow_up_actions.append(ActionWrapper.from_json(follow_up))

        return ActionWrapper(action, size, criteria, symbol, follow_up_actions)


        


