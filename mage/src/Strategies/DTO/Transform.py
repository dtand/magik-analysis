
from mage.src.Services.TransformMappingService import TransformMappingService

class Transform:

    def __init__(self, method='None', configuration={}):
        self.method = method
        self.configuration = configuration

    def from_json(json_object):
        TransformMappingService.is_valid(json_object['method'])        
        return Transform(TransformMappingService.get_transform(json_object['method']), json_object['configuration'])