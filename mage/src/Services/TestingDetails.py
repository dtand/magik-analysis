class TestingDetails:

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.headers = []
        self.rows = []

    def set_headers(self, headers):
        for header in headers:
            self.headers.append(header)
        self.rows.append(headers)

    def add_row(self, info):
        self.rows.append(info)

    def set_time_period(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def export(self):
        return


    

    