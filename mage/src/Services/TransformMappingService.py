import math
from mage.src.Strategies.DTO.Variable import Variable

VALID_TRANSFORMS = ['rsi_inverse_range']

class TransformMappingService:

    def get_transform(method):
        
        ## RSI_RANGE_INVERSE
        if method == VALID_TRANSFORMS[0]:
            return TransformMappingService.rsi_inverse_range
        
        raise Exception("Invalid transform method provided: {}, associated transform must be implemented.".format(method))
    
    def is_valid(method):
        if method not in VALID_TRANSFORMS:
            raise Exception('Transform provided is not valid: {}, must be one of: {}'.format(method, VALID_TRANSFORMS))

    def rsi_inverse_range(size, variable_table, configuration):
        RSI_RANGE  = configuration['rsiRange']
        #CLOSE_TO_A_HIGH = [0, 0.008]
        rsi = variable_table.get(Variable(configuration['symbol'], configuration['variables'][0]))
        rsi_normal = ((1/(RSI_RANGE[1] - RSI_RANGE[0])) * (RSI_RANGE[1] - rsi)) * 2.5
        #close_to_high_normal = max(1, (a_high_a_close / CLOSE_TO_A_HIGH[1]) * 1.5)
        size = math.ceil(size * rsi_normal)

        if size > 15:
            return 15
        if size < 5:
            return 5
        
        return size
