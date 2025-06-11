from mage.src.Services.BacktestEngine import BacktestEngine
from mage.src.Services.BacktestService import BacktestService
from mage.src.Services.DTO.BacktestConfig import BacktestConfig
from mage.src.Services.TradingStrategyFactory import TradingStrategyFactory
import argparse
import statistics

# parser = argparse.ArgumentParser(
#     prog='MagiK Backtesting Engine', 
#     description='Performs backtesting of historical market data using user defined strategies'
# )

# parser.add_argument('-s', '--strategy', help='The json file containing the strategy to use')
# parser.add_argument('-i', '--initial_investment', help='Integerfor the initial investment cashflow')
# parser.add_argument('-sy', '--symbols', help='Comma delimitted list of symbols used int the backtest, ie. TSLA,SPX,PTON')


def main():
    # # args = parser.parse_args()
    # backtesting_engine = BacktestEngine(0)
    # backtesting_engine.prepare('DeltaRSIThreshold.json', ['6B.FUT'])
    # backtesting_engine.execute()
    # #trading_report.print()
    # print("BUYS = {}, SELLS = {}, PNL = {}".format(backtesting_engine.buys, backtesting_engine.sells, backtesting_engine.pnl))
    # print("WIN/LOSS = {}/{}".format(len(backtesting_engine.winners), len(backtesting_engine.losers)))
    # print("AVG WIN = {}, AVG LOSS: = {}".format(statistics.mean(backtesting_engine.winners), statistics.mean(backtesting_engine.losers)))
    # print("AVG WIN / AVG LOSS: {}".format(float(statistics.mean(backtesting_engine.winners)/ (statistics.mean(backtesting_engine.losers)*-1))))
    # backtesting_engine.write_report()


    backtest_config = BacktestConfig(symbols=['6B.FUT'], total_runs=50, sample_size='3M', enable_reports=True, sampling_type='RANDOM', strategy_json='./Strategies/resources/DeltaRSIThresholdLong.json', testing_period=[None, None])
    backtest = BacktestService()
    backtest.config = backtest_config
    backtest.engine = BacktestEngine()
    backtest.run()

    #TradingStrategyFactory.from_json('Test.json')
if __name__ == '__main__':
    main()