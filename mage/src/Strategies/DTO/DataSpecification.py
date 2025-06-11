from mage.src.Strategies.DTO.Indicator import Indicator
from datetime import datetime
VALID_TIME_SERIES = ['1d', '1h']

class DataSpecification:

    def __init__(self, symbol=None, source='LocalFiles', market_type=None, time_series=None, indicators=[], start_date=None, end_date=None):
        self.symbol = symbol
        self.source = source
        self.market_type = market_type
        self.time_series = time_series
        self.indicators = indicators
        self.start_date = start_date
        self.end_date = end_date

    def from_json(json_object):

        if json_object['timeSeries'] not in VALID_TIME_SERIES:
            raise Exception("Invalid time series provided: {}, must be one of: {}".format(json_object['timeSeries'], VALID_TIME_SERIES))
        
        indicators = []
        start_date = None
        end_date = None

        ## Optional: indicators
        if 'indicators' in json_object:
            for indicator in json_object['indicators']:
                indicators.append(Indicator.from_json(indicator))

        ## Optional: startDate
        if 'startDate' in json_object:
            start_date = datetime.strptime(json_object['startDate'], "%Y-%m-%d %H:%M:%S%z")
        
        ## Optional: endDate
        if 'endDate' in json_object:
            end_date = datetime.strptime(json_object['endDate'], "%Y-%m-%d %H:%M:%S%z")
        
        return DataSpecification(json_object['symbol'], json_object['source'], json_object['marketType'], json_object['timeSeries'], indicators, start_date, end_date)