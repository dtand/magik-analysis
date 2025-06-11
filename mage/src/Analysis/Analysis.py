

class Analysis:

    def __init__(self):
        self.name = None
        self.description = None
        self.data_specifications = []
        self.analysis_specification = None
        self.output_specification = None

class DataSpecification:

    def __init__(self):
        self.symbol = None
        self.source = "LocalFiles"
        self.market_type = None
        self.time_series = None
        self.indicators = []

class Indicator:

    def __init__(self):
        self.name = None
        self.identifier = None
        self.config = {}
        self.depends_on = None

class Variable:

    def __init__(self):
        self.symbol = None
        self.var = None
        self.lookahead = 0

class AnalysisSpecification:

    def __init__(self):
        self.criteria = None
        self.predict = None
        self.assess_on = None

class OutputSpecification:

    def __init__(self):
        self.format = 'csv'
        self.variables = []

class Criteria:

    def __init__(self):
      self.var1 = None
      self.op = None
      self.var2 = None
      self.and_ops = []
      self.or_ops = []
        