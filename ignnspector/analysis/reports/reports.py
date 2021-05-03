from abc import ABC, abstractmethod
import yaml

class Report(ABC):
    def __init__(self, report_string:str=None, contents:dict=None):
        if report_string != None:
            self.contents = self.parse_yaml(report_string)
        elif contents != None:
            self.contents = contents

    def yaml_string(self):
        return yaml.dump(self.contents)

    @abstractmethod
    def parse_yaml(self, report_string):
        pass

class GraphReport(Report):
    def __init__(self, report_string=None,  contents:dict=None):
        super(GraphReport, self).__init__(report_string, contents)

    def parse_yaml(self, report_string):
        return yaml.safe_load(report_string)
        # lines = [line.split(': ') 
        #         for line in self.string.splitlines() 
        #         if len(line) > 0 and (line[0] != '#' or line[0] != '-')]
        
        # self.contents = {line[0]:line[1] for line in lines if len(line) == 2}


class ModelReport(Report):
    def __init__(self, report_string=None, contents:dict=None):
        super(ModelReport, self).__init__(report_string, contents)

    def parse_yaml(self, report_string):
        return yaml.safe_load(report_string)

    def premade(self, proposal):
        with open('premade/' + proposal['model_type'] + '.yaml') as f:
            self.report_string = f.read()
            self.parse_yaml()
