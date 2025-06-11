import talib
from mage.src.Indicators.SessionBased import SessionBased
from mage.src.Indicators.Custom import Custom
from mage.src.Indicators.Volume import Volume
from mage.src.Utils.data_utils import extract_values
import numpy as np

def TA(indicator, config, ohlcv):

    match indicator:

        ## Simple moving average
        case "sma":
            sma = talib.SMA(ohlcv[config['real']], timeperiod=config['timeperiod'])
            return { 
                "sma": sma 
            }
        
        ## Exponential moving average
        case "ema":
            ema = talib.EMA(ohlcv['close'], timeperiod=config['timeperiod'])
            return {
                "ema": ema
            }
        
        ## Bollanger Bands
        case "bbands":
            upper, middle, lower = talib.BBANDS(ohlcv['close'], matype=talib.MA_Type.T3)
            return {
                "bbands": {
                    "upper": upper,
                    "middle": middle,
                    "lower": lower
                }
            }

        ## Momentum - Average Directional Movement Index
        case "adx":
            adx = talib.ADX(ohlcv['high'], ohlcv['low'], ohlcv['close'], timeperiod=config['timeperiod'])
            return {
                "adx": adx
            }

        ## Momentum - Average Directional Movement Index Rating
        case "adxr":
            adxr = talib.ADXR(ohlcv['high'], ohlcv['low'], ohlcv['close'], timeperiod=config['timeperiod'])
            return {
                "adxr": adxr
            }

        ## Momentum - Absolute Price Oscillator
        case  "apo":
            apo = talib.APO(ohlcv['close'], fastperiod=12, slowperiod=26, matype=0)
            return {
                "apo": apo
            }
        
        case "plus_di":
            plus_di = talib.PLUS_DI(ohlcv['high'], ohlcv['low'], ohlcv['close'], timeperiod=config['timeperiod'])
            return {
                "plus_di": plus_di
            }

        case "minus_di":
            minus_di = talib.MINUS_DI(ohlcv['high'], ohlcv['low'], ohlcv['close'], timeperiod=config['timeperiod'])
            return {
                "minus_di": minus_di
            }
        
        ## Momentum - Relative Strength Index
        case "rsi": 
            rsi = talib.RSI(ohlcv[config['real']], timeperiod=config['timeperiod'])
            return {
                'rsi': rsi
            }
        
        
        ## Custom - Session Based High
        case "sbh":
            psh, ash, bsh = SessionBased.SBH(ohlcv['high'], ohlcv['timestamp'], pre_session=config['pre_session'], session_a=config['session_a'], session_b=config['session_b'])
            return {
                'sbh': {
                    'psh': psh,
                    'ash': ash,
                    'bsh': bsh
                }
            }
        
        ## Custom - Session Based Low
        case "sbl":
            psl, asl, bsl = SessionBased.SBL(ohlcv['low'], ohlcv['timestamp'], pre_session=config['pre_session'], session_a=config['session_a'], session_b=config['session_b'])
            return {
                'sbl': {
                    'psl': psl,
                    'asl': asl,
                    'bsl': bsl
                }
            }
        
        
        ## Custom - Session Based Open to Close
        case "sbotc":
            potc, aotc, botc = SessionBased.SBOTC(ohlcv['open'], ohlcv['close'], ohlcv['timestamp'], pre_session=config['pre_session'], session_a=config['session_a'], session_b=config['session_b'])
            return {
                'sbotc': {
                    'potc': potc,
                    'aotc': aotc,
                    'botc': botc
                }
            }
        
        # ## Custom - Session Based Open to Session Based High
        # case "sboth": 
        #     #DEPENDS_ON(ohlcv, "sbh")
        #     poth, aoth, both = SessionBased.SBOTH(ohlcv['open'], ohlcv[depends_on], ohlcv['timestamp'], pre_session=config['pre_session'], session_a=config['session_a'], session_b=config['session_b'])
        #     return {
        #         'sboth': {
        #             'poth': poth,
        #             'aoth': aoth,
        #             'both': both
        #         }
        #     }
        
        # ## Custom - Session Based Open to Session Based High
        # case "sbotl": 
        #     #DEPENDS_ON(ohlcv, "sbh")
        #     potl, aotl, botl = SessionBased.SBOTL(ohlcv['open'], ohlcv[depends_on], ohlcv['timestamp'], pre_session=config['pre_session'], session_a=config['session_a'], session_b=config['session_b'])
        #     return {
        #         'sbotl': {
        #             'potl': potl,
        #             'aotl': aotl,
        #             'botl': botl
        #         }
        #     }
        
        ## Custom - Delta 
        case "delta":
            delta = Custom.DELTA(ohlcv[config['indicator']], config['d1'], config['d2'])
            return {
                'delta': delta
            }
        
        ## Custom - Delta 
        case "delta_pct":
            delta = Custom.DELTA(ohlcv[config['indicator']], config['d1'], config['d2'])
            return {
                'delta': delta
            }
        
        ## Custom - Var Change Percent 
        case "var_change_pct":
            var_change_pct = Custom.VAR_CHANGE_PTC(extract_values(ohlcv, config['varX']), extract_values(ohlcv, config['varY']))
            return {
                'var_change_pct': var_change_pct
            }
        
        ## Custom - Real
        case "real":
            real = Custom.REAL(ohlcv['close'], ohlcv['high'], ohlcv['low'])
            return {
                'real': real
            }
        
        ## Volume - On Balance Volume
        case "obv":
            obv = talib.OBV(ohlcv['close'], ohlcv['volume'])
            return {
                "obv": obv
            }
        
        ## Volume - Volume Weighted Average Price
        case "vwap":
            vwap = Volume.VWAP(ohlcv['close'], ohlcv['high'], ohlcv['low'], ohlcv['volume'], config['timeperiod'])
            return {
                "vwap": vwap
            }
        
    raise("Indicator not supported: {}".format(indicator))
        
def DEPENDS_ON(ohlcv, indicator):
    if indicator not in ohlcv:
        raise Exception("Missing dependent indicator: {}".format(indicator))