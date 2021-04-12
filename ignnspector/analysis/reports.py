from abc import ABC, abstractmethod

class Report(ABC):
    def __init__(self, report_file: str=None):
        self.contents = {}
        if report_file != None:
            self.file = report_file
        else:
            self.file = ""

    @abstractmethod
    def parse_file(self, report_file):
        pass

class GraphReport(Report):
    def __init__(self, report_file=None):
        super(GraphReport, self).__init__(report_file)
        self.parse_file()

    def parse_file(self):
        lines = [line.split(': ') 
                for line in self.file.splitlines() 
                if len(line) > 0 and (line[0] != '#' or line[0] != '-')]
        
        self.contents = {line[0]:line[1] for line in lines if len(line) == 2}


class ModelReport(Report):
    def __init__(self):
        pass