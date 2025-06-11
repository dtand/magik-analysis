from mage.src.Services.AnalysisJsonParser import AnalysisJsonParser
from mage.src.Services.DataPrepService import DataPrepService
from mage.src.Services.LogicEngine import LogicEngine
from mage.src.Services.VariableTable import VariableTable
from mage.src.Services.CSVService import CSVService
from mage.src.Utils.json_utils import create_json_from_template

OUTPUT_PATH = "./Analysis/results/"

class AnalysisResult:

    def __init__(self, count_assessed, count_predict):
        self.count_assessed = count_assessed
        self.count_predict = count_predict
        self.probability = round(float(self.count_predict) / float(self.count_assessed),2)

class AnalysisEngine:

    def __init__(self):
        self.analysis = None
        self.data = None
        self.symbols = []
        self.curr_epoch = 0
        self.variable_table = None
        self.count_criteria = 0
        self.count_predict = 0
        self.csv_service = CSVService()
        self.output_data = []
        self.results = []

    def prepare_from_template(self, template, variables):
        create_json_from_template(template, variables)

    def prepare(self, analysis, symbols):
        self.analysis = analysis
        self.data = DataPrepService.get_data(self.analysis.data_specifications)
        self.symbols = symbols
        for symbol in symbols:
            for data_spec in self.analysis.data_specifications:
                if data_spec.symbol == symbol:
                    self.data[symbol] = DataPrepService.inject_indicator_data(data_spec.indicators, self.data[symbol])
        if len(symbols) == 2:
            d1,d2 = DataPrepService.align_data(self.data[symbols[0]], self.data[symbols[1]])
            self.data[symbols[0]] = d1
            self.data[symbols[1]] = d2

    def write_output(self, result):
        self.csv_service.add_page(self.symbols[0])
        self.csv_service.add_row(self.symbols[0], ['Probability'])
        self.csv_service.add_row(self.symbols[0], [result])
        output_arr = []
        for var in self.analysis.output_specification.variables:
            if var.lookahead == 0:
                output_arr.append(var.symbol + "-" + var.var)
            else:
                output_arr.append(var.symbol + "-" + var.var + str(var.lookahead))

        output_arr.append("Criteria Result")
        output_arr.append("Predict Result")
        output_arr.append("Hit")
        self.csv_service.add_row(self.symbols[0], output_arr)
        for row in self.output_data:
            self.csv_service.add_row(self.symbols[0], row)

    def execute(self):
        #print("Performing analysis on {}...".format(self.symbols[0]))
        core_symbol = self.analysis.data_specifications[0].symbol
        total_epochs = len(self.data[core_symbol]['open'])
        for i in range(0, total_epochs):
            self.curr_epoch = i
            self.epoch()
        probability = round(float(self.count_predict) / float(self.count_criteria),2)
        self.write_output(probability)
        self.csv_service.write_to_folder(OUTPUT_PATH)
        # self.csv_service.to_workbook(OUTPUT_PATH, OUTPUT_PATH + 'RESULTS.xlsx')
        return AnalysisResult(self.count_criteria, self.count_predict)
        
    def epoch(self):
        variable_table = VariableTable.for_analysis(self)
        #print("{},{}".format(self.data['6B.FUT']['timestamp'][self.curr_epoch], self.data['6B.FUT']['RSI'][self.curr_epoch]))
        if LogicEngine.assess_statement(self.analysis.analysis_specification.assess_on, variable_table):
            criteria_result, predict_result = self.assess_criteria(variable_table)
            self.add_row(criteria_result, predict_result, variable_table)

    def assess_criteria(self, variable_table):
        
        criteria = self.analysis.analysis_specification.criteria
        precict = self.analysis.analysis_specification.predict
        criteria_result = LogicEngine.assess_statement(criteria, variable_table)
        predict_result = LogicEngine.assess_statement(precict, variable_table) 

        if criteria_result:
            self.count_criteria = self.count_criteria + 1

        if criteria_result and predict_result:
            self.count_predict = self.count_predict + 1

        self.curr_epoch = self.curr_epoch + 1

        return criteria_result, predict_result

    def add_row(self, criteria_result, predict_result, variable_table):
        hit = predict_result and criteria_result
        out_data = []
        out_map = {}
        for var in self.analysis.output_specification.variables: 
            out_data.append(str(variable_table.get(var)))
            out_map[var.var] = variable_table.get(var)
        out_data.append(str(criteria_result))
        out_data.append(str(predict_result))
        out_map['CRITERIA'] = criteria_result
        out_map['RESULT'] = predict_result
        if hit:
            out_map['HIT'] = 'X'
            out_data.append('X')
        self.output_data.append(out_data)
        self.results.append(out_map)


