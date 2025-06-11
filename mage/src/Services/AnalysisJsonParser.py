import json
from mage.src.Analysis.Analysis import *

class AnalysisJsonParser:

    def do_parse(filename, symbols):
        data = None

        with open('Analysis/resources/{}'.format(filename), 'r') as file:
            data = json.load(file)

        analysis = Analysis()
        
        analysis.name = data['name']
        analysis.description = data['description']

        for data_spec_json in data['dataSpecifications']:
            data_spec = DataSpecification()
            data_spec.market_type =  data_spec_json['marketType']
            data_spec.symbol = AnalysisJsonParser.replace_symbol(data_spec_json['symbol'], symbols)
            data_spec.time_series =  data_spec_json['timeSeries']
            data_spec.source = data_spec_json['source']
            for indicator in data_spec_json['indicators']:
                strategy_indicator = Indicator()
                strategy_indicator.identifier  = indicator['identifier']
                strategy_indicator.name = indicator['name']
                strategy_indicator.config = indicator['config']
                if 'dependsOn' in indicator:
                    strategy_indicator.depends_on = indicator['dependsOn']
                data_spec.indicators.append(strategy_indicator)
            analysis.data_specifications.append(data_spec)

        analysis_specification = data['analysisSpecification']

        spec_criteria = None
        spec_predict = None
        
        if 'criteria' in analysis_specification:
            spec_criteria = AnalysisJsonParser.parse_criteria(analysis_specification['criteria'], symbols)
        if 'predict' in analysis_specification:
            spec_predict = AnalysisJsonParser.parse_criteria(analysis_specification['predict'], symbols)

        assess_on = AnalysisJsonParser.parse_criteria(analysis_specification['assessOn'], symbols)

        analysis.analysis_specification = AnalysisSpecification()
        analysis.analysis_specification.criteria = spec_criteria
        analysis.analysis_specification.predict = spec_predict
        analysis.analysis_specification.assess_on = assess_on

        output_specification = data['outputSpecification']
        analysis.output_specification = OutputSpecification()
        analysis.output_specification.format = output_specification['format']
        for var in output_specification['variables']:
            var_obj = Variable()
            var_obj.var = var['var']
            var_obj.symbol = AnalysisJsonParser.replace_symbol(var['symbol'],symbols)
            var_obj.lookahead = var['lookahead']
            analysis.output_specification.variables.append(var_obj)
        return analysis

    def parse_criteria(criteria_dict, symbols):
            
            criteria = Criteria()

            var1 = Variable()
            var2 = Variable()

            var1.symbol = AnalysisJsonParser.replace_symbol(criteria_dict['var1']['symbol'], symbols)
            var1.var = criteria_dict['var1']['var']
            var1.lookahead = criteria_dict['var1']['lookahead']

            var2.symbol = AnalysisJsonParser.replace_symbol(criteria_dict['var2']['symbol'], symbols)
            var2.var = criteria_dict['var2']['var']
            var2.lookahead = criteria_dict['var2']['lookahead']

            criteria.var1 = var1
            criteria.op = criteria_dict['op']
            criteria.var2 = var2

            if "and" in criteria_dict:
                for and_criteria in criteria_dict["and"]:
                    criteria.and_ops.append(AnalysisJsonParser.parse_criteria(and_criteria, symbols))
            else:
                criteria.and_ops = []

            if "or" in criteria_dict:
                for or_criteria in criteria_dict["or"]:
                    criteria.or_ops.append(AnalysisJsonParser.parse_criteria(or_criteria, symbols))
            else:
                criteria.or_ops = []
            
            return criteria

    def replace_symbol(value, symbols):
        if type(value) is not str:
            return value
        if '$' in value:
            return symbols[int(value.strip('$'))-1]
        return value
