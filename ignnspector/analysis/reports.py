

class Report:
    def __init__(self, report_file: str=None):
        self.contents = {} # Aquí hi ha una entrada per cada component que conforma un report
        if report_file != None:
            self.file = report_file
        else:
            self.file = ""

    def parse_file(self):
        pass

class GraphReport(Report):
    def __init__(self, report_file=None):
        super(GraphReport, self).__init__(report_file)
        self.parse_file()

    def parse_file(self):
        lines = [line.split(': ') for line in self.file.splitlines()]
        lines = lines[2:]
        self.contents = {line[0]:line[1] for line in lines if len(line) == 2}


class ModelReport(Report):
    def __init__(self):
        pass