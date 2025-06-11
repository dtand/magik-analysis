
from mage.src.Strategies.DTO.DataSpecification import DataSpecification
from mage.src.Strategies.DTO.ActionWrapper import ActionWrapper
from mage.src.Strategies.DTO.Signal import Signal

class TradingStrategy:

    def __init__(self, name='Test', description='', data_specifications=[], actions=[], signals=[]):
        self.name = name
        self.description = description
        self.data_specifications = data_specifications
        self.actions = actions
        self.signals = signals

    def from_json(json_object):
        data_specs = []
        actions = []
        signals = []

        for data_spec in json_object['dataSpecifications']:
            data_specs.append(DataSpecification.from_json(data_spec))

        for action in json_object['actions']:
            actions.append(ActionWrapper.from_json(action))

        for signal in json_object['signals']:
            signals.append(Signal.from_json(signal))
                                
        return TradingStrategy(json_object['name'], json_object['description'], data_specs, actions, signals)

        

