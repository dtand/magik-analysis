from mage.src.Strategies.DTO.Transform import Transform
from mage.src.Services.TransformMappingService import TransformMappingService

VALID_TYPES = ['PERCENT', 'STANDARD']

class OrderSize:

    def __init__(self, size="", type='STANDARD', transform=None):
        self.size = size
        self.type = type
        self.transform = transform

    def from_json(json_object):

        if json_object['type'] not in VALID_TYPES:
            raise Exception("Invalid type provided: {}, must be one of: {}".format(json_object['type'], VALID_TYPES))

        ## Optional: transform
        transform = None
        if 'transform' in json_object:
            transform = Transform.from_json(json_object['transform'])

        return OrderSize(json_object['size'], json_object['type'], transform)

    def get_real_size(self, open_position=None, variable_table=None):

        size = self.size

        if self.transform != None:
            size = self.transform.method(size, variable_table, self.transform.configuration)

        elif self.type == 'PERCENT':
            if open_position == None:
                raise Exception("PERCENT type order requires open position")
            size = open_position.quantity * size

        return size
        


