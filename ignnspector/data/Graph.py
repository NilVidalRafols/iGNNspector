from ignnspector.analysis.reports import GraphReport

class Graph:
    def __init__(self, report:[GraphReport]=None):
        if report != None:
            self.report = report
        else:
            self.report = GraphReport()