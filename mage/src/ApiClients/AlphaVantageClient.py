import requests

class AlphaVantage:
    
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={0}&outputsize={1}&apikey={2}&dataset={3}&adjusted=true"

    def __init__(self, api_key):
        self.api_key = api_key

    def time_series_daily(self, symbol, output_size='full', dataset='json'):
        r = requests.get(AlphaVantage.url.format(symbol, output_size, self.api_key, dataset))
        return r.json()

