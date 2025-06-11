from mage.src.Strategies.DTO.Variable import Variable

VALID_OPERATIONS = ['gt', 'lt', 'eq', 'lteq', 'gteq']

class Criteria:

    def __init__(self, var1=None, op=None, var2=None, and_ops=[], or_ops=[]):
        self.var1 = var1
        self.op = op
        self.var2 = var2
        self.and_ops = and_ops
        self.or_ops = or_ops

    def from_json(json_object):
        var1 = Variable.from_json(json_object['var1'])
        op = json_object['op']
        var2 = Variable.from_json(json_object['var2'])

        ## Optional: and_ops
        and_ops = []
        if 'and' in json_object:
            for criteria in json_object['and']:
                and_op = Criteria.from_json(criteria)
                and_ops.append(and_op)

        ## Optional: or_ops
        or_ops = []
        if 'or' in json_object:
            for criteria in json_object['or']:
                or_op = Criteria.from_json(criteria)
                or_ops.append(or_op)

        if op not in VALID_OPERATIONS:
            raise Exception("Invalid op provided: {}, value must be one of: {}".format(op, VALID_OPERATIONS))
        
        return Criteria(var1, op, var2, and_ops, or_ops)

    