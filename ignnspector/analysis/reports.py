from abc import ABC, abstractmethod
import yaml

class Report(ABC):
    def __init__(self, report_string: str=None):
        self.contents = {}
        if report_string != None:
            self.string = report_string
        else:
            self.string = ""

    @abstractmethod
    def parse_string(self, report_string):
        pass

class GraphReport(Report):
    def __init__(self, report_string=None):
        super(GraphReport, self).__init__(report_string)
        self.parse_string()

    def parse_string(self):
        lines = [line.split(': ') 
                for line in self.string.splitlines() 
                if len(line) > 0 and (line[0] != '#' or line[0] != '-')]
        
        self.contents = {line[0]:line[1] for line in lines if len(line) == 2}


class ModelReport(Report):
    def __init__(self, report_string=None):
        super(ModelReport, self).__init__(report_string)
        self.parse_string()

    def parse_string(self):
        self.contents = yaml.safe_load(self.string)
