import json

class BacktestConfig:

    def __init__(self, symbols=[], total_runs=1, sample_size='ALL', enable_reports=True, sampling_type='SEQUENTIAL', strategy_json='Test.json', testing_period=[None, None]):
        self.symbols = symbols
        self.total_runs = total_runs
        self.sample_size = sample_size
        self.enable_reports = enable_reports
        self.sampling_type = sampling_type
        self.strategy_json = strategy_json
        self.testing_period = testing_period
    
    def from_json(json_file):
        with open('Services/resources/{}'.format(json_file), 'r') as file:
            data = json.load(file)
        return BacktestConfig(data['symbols'], data['totalRuns'], data['sampleSize'], data['enableReports'], data['samplingType'], data['strategyJson'], data['testingPeriod'])