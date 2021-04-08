

class Report:
    __init__(self, report_file:str=None):
    self.contents = {} # Aquí hi ha una entrada per cada component que conforma un report
    if report_file != None:
        self.file = report_file
    else
        self.file = ""

    def parse_file(self):
        pass

class GraphReport(Report):
    __init__(self, report_file=None):
        super(GraphReport, self).__init__(report_file)

    def parse_file(self):
        lines = [line.split(': ') for line in self.file.splitlines()]
        lines = [2:]
        self.contents = {metric:value for (metric, value) in lines}


class ModelReport(Report):
    __init__(self):
