
class Indicator:

    def __init__(self, name=None, identifier=None, config={}):
        self.name = name
        self.identifier = identifier
        self.config = config

    def from_json(json_object):

        if '.' in json_object['identifier']:
            raise Exception("Invalid identifier provided: {}, may not contain '.' character".format(json_object['identifier']))
        
        return Indicator(json_object['name'], json_object['identifier'], json_object['config'])