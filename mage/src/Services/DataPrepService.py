
from mage.src.ApiClients.AlphaVantageClient import AlphaVantage
from mage.src.Services.TA import TA
from mage.src.Services.LocalDataCaching import LocalDataCaching
import numpy as np
import json
import os
import csv
from collections import OrderedDict
from datetime import datetime, timezone
from mage.src.Utils.data_utils import empty_data_from_keys

LOCAL_CACHING_ENABLED = True
DATA_SOURCE_MAPPINGS_FILE = 'Resources/data-mappings.json'
alphaVantageClient = AlphaVantage("JH59FM1XYEHMXHDJ")

class DataPrepService:

    data_source_mappings = json.load(open(DATA_SOURCE_MAPPINGS_FILE, 'r'))


    def get_data(data_specifications):

        data = {}
        symbols = []

        for data_spec in data_specifications:
            symbol = data_spec.symbol
            symbols.append(symbol)
            time_series = data_spec.time_series
            source = data_spec.source

            if source == "AlphaVantage":
                data[symbol] = DataPrepService.from_alpha_vantage(symbol)
            else:
                #data[symbol] = DataPrepService.from_local_files(symbol, time_series, start_ts=datetime.fromtimestamp(1577840400, timezone.utc))
                #data[symbol] = DataPrepService.from_local_files(symbol, time_series) 1706736000
                #data[symbol] = DataPrepService.from_local_files(symbol, time_series, start_ts=datetime.fromtimestamp(1706736000, timezone.utc), end_ts=datetime.fromtimestamp(1714688400, timezone.utc))
                data[symbol] = DataPrepService.from_local_files(symbol, time_series, start_ts=data_spec.start_date, end_ts=data_spec.end_date)

            if LOCAL_CACHING_ENABLED and data_spec.source != 'LocalFiles':
                for symbol in data:
                    print("Update local cache for dataset: {}-{}".format(symbol, "DAILY"))
                    LocalDataCaching.store(symbol, "DAILY", data)

        for symbol in symbols:
            for data_spec in data_specifications:
                if data_spec.symbol == symbol:
                    data[symbol] = DataPrepService.inject_indicator_data(data_spec.indicators, data[symbol])

        return data
            
    def from_local_files_bulk(symbols, time_series, start_ts=None, end_ts=None):
        
        if start_ts == None:
            start_ts = datetime.fromtimestamp(0, timezone.utc)
        if end_ts == None:
            end_ts = datetime.now(timezone.utc)

        data = {}
        for symbol in symbols:
            local_data = None
            symbol_data = DataPrepService.ohlcv_dict()
            with open('./Resources/test-data/{}-{}.json'.format(symbol, time_series), 'r') as file:
                local_data = json.load(file)
            for ohlcv in local_data:
                DataPrepService.map_ohlcv(symbol_data, ohlcv, DataPrepService.data_source_mappings["LocalFiles"])
            data[symbol] =DataPrepService.filter_data(symbol_data, start_ts, end_ts) 
        return data
    
    def from_local_files(symbol, time_series, start_ts=None, end_ts=None):
        if start_ts == None:
            start_ts = datetime.fromtimestamp(0, timezone.utc)
        if end_ts == None:
            end_ts = datetime.now(timezone.utc)

        data = {}
        local_data = None
        symbol_data = DataPrepService.ohlcv_dict()
        with open('./Resources/test-data/{}-{}.json'.format(symbol, time_series), 'r') as file:
            local_data = json.load(file)
        for ohlcv in local_data:
            DataPrepService.map_ohlcv(symbol_data, ohlcv, DataPrepService.data_source_mappings["LocalFiles"])
        return DataPrepService.filter_data(symbol_data, start_ts, end_ts) 

    def from_alpha_vantage(symbol):
        
        resp = alphaVantageClient.time_series_daily(symbol)
        data = DataPrepService.ohlcv_dict()

        for key in resp["Time Series (Daily)"]: 
            ohlcv = resp["Time Series (Daily)"][key]
            ohlcv['timestamp'] = key
            DataPrepService.map_ohlcv(data, ohlcv, DataPrepService.data_source_mappings["AlphaVantage"])

        data['open'] = np.flip(data['open'])
        data['high'] = np.flip(data['high'])
        data['low'] = np.flip(data['low'])
        data['close'] = np.flip(data['close'])
        data['volume'] = np.flip(data['volume'])
        data['timestamp'] = np.flip(data['timestamp'])    
        
        return data
    
    def from_databento_futures():
        files = os.listdir('./Resources/downloads/databento')
        rolling_data = {}

        for file in files:
            if '.csv' not in file:
                continue
            symbology_file = './Resources/downloads/databento/' + file.replace('.ohlcv','.symbols').replace('.csv','.json')
            fut_mappings = DataPrepService.parse_future_symbols(symbology_file)
            sym_ts_lookup = {}
            with open('./Resources/downloads/databento/' + file, 'r') as f:
                csvreader = csv.reader(f)
                next(csvreader, None)

                ## Iterate all rows in csv to create a 'rolling' future contract for each symbol
                for row in csvreader:

                    ## Symbol for specific contract including month and year, ignore spreads
                    contract_sym = row[9]
                    if '-' in contract_sym or ':' in contract_sym or ' ' in contract_sym:
                        continue

                    ## Global symbol for entire future's life postfixed with .FUT
                    fut_sym = fut_mappings[contract_sym]
                    
                    ts = datetime.fromisoformat(row[0])
                    ## Init lookup SYM.FUT -> TS 
                    if fut_sym not in sym_ts_lookup:
                        sym_ts_lookup[fut_sym] = OrderedDict()

                    ## Update SYM.FUT -> TS -> row w/ timestamp mapped row w/ greatest volume
                    if ts not in sym_ts_lookup[fut_sym]:
                        sym_ts_lookup[fut_sym][ts] = row
                    else:
                        curr_vol = float(row[8])
                        map_vol = float(sym_ts_lookup[fut_sym][ts][8])
                        if curr_vol > map_vol:
                            sym_ts_lookup[fut_sym][ts] = row

            ## Build continuous / rolling dataset for each set of futures  
            for symbol in sym_ts_lookup:
                if symbol not in rolling_data:
                    rolling_data[symbol] = {
                        'open': np.array([]),
                        'low': np.array([]),
                        'high': np.array([]), 
                        'close': np.array([]), 
                        'volume': np.array([]),
                        'timestamp': np.array([]),
                        'contract': np.array([])
                    }
                for key, row in sym_ts_lookup[symbol].items():
                    rolling_data[symbol]['open'] = np.append(rolling_data[symbol]['open'], float(row[4]))
                    rolling_data[symbol]['low'] = np.append(rolling_data[symbol]['low'], float(row[6]))
                    rolling_data[symbol]['high'] = np.append(rolling_data[symbol]['high'], float(row[5]))
                    rolling_data[symbol]['close']= np.append(rolling_data[symbol]['close'], float(row[7]))
                    rolling_data[symbol]['volume'] = np.append(rolling_data[symbol]['volume'], float(row[8]))
                    rolling_data[symbol]['timestamp'] = np.append(rolling_data[symbol]['timestamp'], key)
                    rolling_data[symbol]['contract'] = np.append(rolling_data[symbol]['contract'], row[9])
            
        return rolling_data

    def parse_future_symbols(symbology_json):
        data = None
        fut_mappings = {}
        with open(symbology_json, "r") as file:
            data = json.load(file)
            symbols_list = data['symbols']
            partial_list = data['partial']
            for partial in partial_list:
                for fut_sym in symbols_list:
                    if '-' in partial:
                        syms = partial.split('-')
                        if DataPrepService.check_first_characters(syms[0], fut_sym):
                            fut_mappings[syms[0]] = fut_sym
                        if DataPrepService.check_first_characters(syms[1], fut_sym):
                            fut_mappings[syms[1]] = fut_sym
                    elif ':' not in partial and DataPrepService.check_first_characters(partial, fut_sym):
                        fut_mappings[partial] = fut_sym 
        return fut_mappings
    
    def check_first_characters(contract, future):
        fut_sym = future.replace('.FUT', '')
        x = len(fut_sym)
        if x > len(contract):
            return False
        return contract[:x] == fut_sym[:x]


    def from_crypto_data_download():
        files = os.listdir('./Resources/downloads/crypto_download/')
        data = {}
        for file in files:
            with open('./Resources/downloads/crypto_download/' + file, 'r') as f:
                symbol = file.split('_')[1]
                csvreader = csv.reader(f)
                next(csvreader, None)
                for row in csvreader:
                    if symbol not in data:
                        data[symbol] = {
                            'open': np.array([]),
                            'low': np.array([]),
                            'high': np.array([]), 
                            'close': np.array([]), 
                            'volume': np.array([]),
                            'timestamp': np.array([])
                        }
                    dt = None
                    try:
                        if 'Binance' in file:    
                            dt = datetime.fromtimestamp(int(int(row[0])/1000), timezone.utc)
                        else:
                            dt = datetime.fromtimestamp(int(int(row[0])), timezone.utc)
                    except:
                        continue
                    data[symbol]['open'] = np.append(data[symbol]['open'], float(row[3]))
                    data[symbol]['low'] = np.append(data[symbol]['low'], float(row[5]))
                    data[symbol]['high'] = np.append(data[symbol]['high'], float(row[4]))
                    data[symbol]['close']= np.append(data[symbol]['close'], float(row[6]))
                    data[symbol]['volume'] = np.append(data[symbol]['volume'], float(row[8]))
                    data[symbol]['timestamp'] = np.append(data[symbol]['timestamp'], dt)

                data[symbol]['open'] = np.flip(data[symbol]['open'])
                data[symbol]['high'] = np.flip(data[symbol]['high'])
                data[symbol]['low'] = np.flip(data[symbol]['low'])
                data[symbol]['close'] = np.flip(data[symbol]['close'])
                data[symbol]['volume'] = np.flip(data[symbol]['volume'])
                data[symbol]['timestamp'] = np.flip(data[symbol]['timestamp']) 
        return data

    def inject_indicator_data(indicators, data):
        for indicator in indicators:
            result = TA(indicator.name, indicator.config, data)
            for key in result:
                data[indicator.identifier] = result[key]
        return data
    
    def ohlcv_dict():
        return {
            'open': np.array([]),
            'low': np.array([]),
            'high': np.array([]), 
            'close': np.array([]), 
            'volume': np.array([]),
            'timestamp': np.array([])
        }
    
    def map_ohlcv(data, ohlcv, mapping):
        data['open'] = np.append(data['open'], float(ohlcv[mapping['open']]))
        data['high'] = np.append(data['high'], float(ohlcv[mapping['high']]))
        data['low'] = np.append(data['low'], float(ohlcv[mapping['low']]))
        data['close'] = np.append(data['close'], float(ohlcv[mapping['close']]))
        data['volume'] = np.append(data['volume'], float(ohlcv[mapping['volume']]))
        data['timestamp'] = np.append(data['timestamp'], datetime.fromisoformat(ohlcv[mapping['timestamp']]))

    def filter_data(data, start_ts, end_ts):
        new_data = {}
        
        for symbol in data:
            new_data = {
                'open': np.array([]),
                'low': np.array([]),
                'high': np.array([]), 
                'close': np.array([]), 
                'volume': np.array([]),
                'timestamp': np.array([])
            }
            for i in range(0, len(data['timestamp'])):
                ts = data['timestamp'][i]
                if ts >= start_ts and ts <= end_ts:
                    new_data['open'] = np.append(new_data['open'], data['open'][i])
                    new_data['low'] = np.append(new_data['low'], data['low'][i])
                    new_data['high'] = np.append(new_data['high'], data['high'][i])
                    new_data['close']= np.append(new_data['close'], data['close'][i])
                    new_data['volume'] = np.append(new_data['volume'], data['volume'][i])
                    new_data['timestamp'] = np.append(new_data['timestamp'], data['timestamp'][i])

        return new_data
    
    def align_data(d1, d2):
        d1 = DataPrepService._align_data(d1, d2)
        d2 = DataPrepService._align_data(d2, d1)
        return d1, d2
    
    def _align_data(d1, d2):
        new_data = DataPrepService.empty_data_from_keys(d1)
        d2_ts_map = set()
        for ts in d2['timestamp']:
            d2_ts_map.add(ts)

        for i in range(0, len(d1['timestamp'])):
            ts = d1['timestamp'][i]
            if ts in d2_ts_map:
                for key in d1:
                    if isinstance(d1[key], dict):
                        for k in d1[key]:
                            new_data[key][k] = np.append(new_data[key][k], d1[key][k][i])
                    else:
                        new_data[key] = np.append(new_data[key], d1[key][i])

        return new_data
    
