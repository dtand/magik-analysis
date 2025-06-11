from mage.src.Services.BacktestEngine import BacktestEngine
from mage.src.Services.DTO.BacktestConfig import BacktestConfig
from mage.src.Services.TradingStrategyFactory import TradingStrategyFactory
from mage.src.Services.DataPrepService import DataPrepService
from mage.src.Services.DataSamplingService import DataSamplingService

class BacktestService:

    def __init__(self):
        self.config = None
        self.engine = None

    def configure(self, config_json):
        self.config = BacktestConfig.from_json(config_json)

    def run(self):
        
        symbols = self.config.symbols
        strategy = self.get_strategy(symbols)
        data = DataPrepService.get_data(strategy.data_specifications)
        data_samples = []
        
        if self.config.sampling_type != 'NONE':
            ## Engine created using full span of data, and will
            ## run through from start to finish
            if self.config.sampling_type == 'SEQUENTIAL':
                data_samples = DataSamplingService.sample_sequential(data[symbols[0]], self.config.sample_size)

            ## Random samples will be pulled using provided
            ## sample size each sample will be pushed to the
            ## engine
            elif self.config.sampling_type == 'RANDOM':
                data_samples = DataSamplingService.sample_random(data[symbols[0]], self.config.sample_size, self.config.total_runs)

            for sample in data_samples: 
                self.engine = BacktestEngine()
                sampled_dataset = {}
                for symbol in symbols:
                    sampled_dataset[symbol] = sample
                self.engine.init(symbols, strategy, sampled_dataset)
                self.engine.execute()
                self.engine.trading_report.output_report()
        else:
            self.engine.init(symbols, strategy, data)
            self.engine.execute()
            self.engine.write_report()
            self.engine.trading_report.output_report()


    def get_strategy(self, symbols):
        strategy = TradingStrategyFactory.from_json(self.config.strategy_json)
        
        if self.config.testing_period != None:
            for i in range(0, len(strategy.data_specifications)):
                strategy.data_specifications[i].start_date = self.config.testing_period[0]
                strategy.data_specifications[i].end_date = self.config.testing_period[1]

        return strategy
