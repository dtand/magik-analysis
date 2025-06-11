from mage.src.Services.TradingStrategyFactory import TradingStrategyFactory

def test_parse_test_json():
    result = TradingStrategyFactory.from_json('test/resources/Test.json')
    
    ## Global
    assert result.name == 'Test1'
    assert result.description == 'Test1'

    ## Data specification
    assert result.data_specifications[0].symbol == '$1'
    assert result.data_specifications[0].source == 'LocalFiles'
    assert result.data_specifications[0].market_type == 'FUTURE'
    assert result.data_specifications[0].time_series == '1h'
    assert result.data_specifications[0].indicators[0].name == 'rsi'
    assert result.data_specifications[0].indicators[0].identifier == 'RSI'
    assert result.data_specifications[0].indicators[0].config['timeperiod'] == 12
    
    ## Signals
    assert result.signals[0].identifier == 'RSI_ABOVE_50'
    assert result.signals[0].criteria.var1.symbol == '$1'
    assert result.signals[0].criteria.var1.var == 'RSI'
    assert result.signals[0].criteria.var1.symbol == '$1'
    assert result.signals[0].criteria.op == 'gt'
    assert result.signals[0].criteria.var2.symbol == None
    assert result.signals[0].criteria.var2.var == 50

    '''
    {
                "action": {
                    "do": "MARKET_BUY"
                },
                "size": {
                    "size": 10,
                    "type": "STANDARD"
                },
                "symbol": "$1",
                "criteria": {
                    "var1": {
                        "symbol": "$1",
                        "var": "timestamp.hour",
                        "lookahead": 0
                    },
                    "op": "eq",
                    "var2": {
                        "symbol": null,
                        "var": 12,
                        "lookahead": 0
                    },
                    "and": [{
                        "var1": {
                            "symbol": null,
                            "var": "RSI_BULLISH_TREND",
                            "lookahead": 0
                        },
                        "op": "eq",
                        "var2": {
                            "symbol": null,
                            "var": true,
                            "lookahead": 0
                        }                   
                    }]
                },
                "followUpActions": [{
                    "action": {
                        "do": "SIGNAL_RESET"
                    }
                }]
            },
            {
                "action": {
                    "do": "MARKET_SELL"
                },
                "size": {
                    "size": 1.0,
                    "type": "PERCENT"
                },
                "symbol": "$1",
                "criteria": {
                    "var1": {
                        "symbol": "$1",
                        "var": "timestamp.hour",
                        "lookahead": 0
                    },
                    "op": "eq",
                    "var2": {
                        "symbol": null,
                        "var": 20,
                        "lookahead": 0
                    }
                }
            }
    '''

    ## Actions[0]
    assert result.actions[0].action.do == 'MARKET_BUY'
    assert result.actions[0].size.size == 10
    assert result.actions[0].size.type == 'STANDARD'
    assert result.actions[0].symbol == '$1'
    assert result.actions[0].criteria.var1.symbol == '$1'
    assert result.actions[0].criteria.var1.var == 'timestamp.hour'
    assert result.actions[0].criteria.var1.offset == 0
    assert result.actions[0].criteria.op == 'eq'
    assert result.actions[0].criteria.var2.symbol == None
    assert result.actions[0].criteria.var2.var == 12
    assert result.actions[0].criteria.var2.offset == 0
    assert result.actions[0].criteria.and_ops[0].var1.symbol == None
    assert result.actions[0].criteria.and_ops[0].var1.var == 'RSI_BULLISH_TREND'
    assert result.actions[0].criteria.and_ops[0].var1.offset == 0
    assert result.actions[0].criteria.and_ops[0].op == 'eq'
    assert result.actions[0].criteria.and_ops[0].var2.symbol == None
    assert result.actions[0].criteria.and_ops[0].var2.var == True
    assert result.actions[0].criteria.and_ops[0].var1.offset == 0

    ## Actions[1]
    assert result.actions[1].action.do == 'MARKET_SELL'
    assert result.actions[1].size.size == 1.0
    assert result.actions[1].size.type == 'PERCENT'
    assert result.actions[1].symbol == '$1'
    assert result.actions[1].criteria.var1.symbol == '$1'
    assert result.actions[1].criteria.var1.var == 'timestamp.hour'
    assert result.actions[1].criteria.var1.offset == 0
    assert result.actions[1].criteria.op == 'eq'
    assert result.actions[1].criteria.var2.symbol == None
    assert result.actions[1].criteria.var2.var == 20
    assert result.actions[1].criteria.var2.offset == 0


