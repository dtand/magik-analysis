class Entry:

    def __init__(self, action, metadata):
        self.action = action
        self.metadata = metadata


class Report:

    def __init__(self):
        self.variables = []
        self.entries = []

    def add_entry(self, action, metadata):
        self.entries.append(Entry(action, metadata))

