from mage.src.Services.LocalDataCaching import LocalDataCaching
from mage.src.Services.DataPrepService import DataPrepService
import argparse

# parser = argparse.ArgumentParser(
#     prog='Magik Backtesting Engine', 
#     description='Performs backtesting of historical market data using user defined strategies'
# )

# parser.add_argument('-s', '--strategy', help='The json file containing the strategy to use')
# parser.add_argument('-i', '--initial_investment', help='Integerfor the initial investment cashflow')
# parser.add_argument('-sy', '--symbols', help='Comma delimitted list of symbols used int the backtest, ie. TSLA,SPX,PTON')

def main():
    results = DataPrepService.from_databento_futures()
    LocalDataCaching.store_bulk(results, '1h')

if __name__ == '__main__':
    main()