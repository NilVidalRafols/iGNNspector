# python imports

# external imports

# tool imports
from ignnspector.data import Graph
from ignnspector.analysis.reports import *


class Analyzer:

    def __init__(self, graph: Union[Graph,MetricsReport], model: Union[Model, ModelReport]):
        if isinstance(graph, Graph):
            self.graph = graph
        
        if isinstance(model, Model):
            self.model

    def analyse_graph(self, graph:Union[Graph,MetricsReport]=None):
        #self.graph.report = report

    # analitza el model que li has pasat i et diu el nombre de capes el seu tipus etc.
    def analyse_model(self, model: ['''Model'''ModelReport]):
        r"""Analyze a model and writte its corresponding model report
        """

    def propose_model(self):
        metrics = self.graph.report.contents
        

    def compare_models(self, other_model):

