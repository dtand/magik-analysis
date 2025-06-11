import json

class LocalFiles:

    def __init__(self, api_key):
        self.api_key = api_key

    def time_series_daily(self, symbol, output_size='full', dataset='json'):
        filename = '{}-{}-{}.json'.format(symbol, output_size, dataset)
        with open('Resources/test-data/{}'.format(filename), 'r') as file:
            return json.load(file)

