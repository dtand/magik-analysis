from mage.src.Strategies.DTO.Criteria import Criteria

class Signal:

    def __init__(self, identifier, criteria):
        self.identifier = identifier
        self.criteria = criteria

    def from_json(json_object):
        return Signal(json_object['identifier'], Criteria.from_json(json_object['criteria']))