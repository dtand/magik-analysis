import json

class LocalDataCaching:

    def store_bulk(data, time_series):
         for symbol in data:
              LocalDataCaching.store(symbol, time_series, data)

    def store(symbol, time_series, data):
        ohlcv_array = []
        total_candles = len(data[symbol]['open'])
        ohlcv = data[symbol]
        for i in range(0, total_candles): 
            if '.FUT' in symbol:
                ohlcv_array.append({
                    "open": float(ohlcv['open'][i]),
                    "high": float(ohlcv['high'][i]),
                    "low": float(ohlcv['low'][i]),
                    "close": float(ohlcv['close'][i]),
                    "volume": float(ohlcv['volume'][i]),
                    "timestamp": ohlcv['timestamp'][i],
                    'contract': ohlcv['contract'][i]
                })
            else:
                ohlcv_array.append({
                    "open": float(ohlcv['open'][i]),
                    "high": float(ohlcv['high'][i]),
                    "low": float(ohlcv['low'][i]),
                    "close": float(ohlcv['close'][i]),
                    "volume": float(ohlcv['volume'][i]),
                    "timestamp": ohlcv['timestamp'][i]
                })               
        LocalDataCaching.write_local_file("{}-{}.json".format(symbol, time_series), ohlcv_array)
    
    def write_local_file(filename, data):
        with open('Resources/test-data/{}'.format(filename), 'w+') as file:
                json.dump(data, file, indent=4, default=str)