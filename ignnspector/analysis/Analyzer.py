# python imports

# external imports

# tool imports
from ignnspector.data import Graph
from ignnspector.analysis.reports import *
from ignnspector.analysis.proposers import *


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

    def propose_model_using(self, proposer_name:Union[str,Proposer]=None):
        metrics = self.graph.report.contents
        
        if type(proposer_name) == str:
            try:
                proposer = eval(proposer_name)
            except NameError as err:
                raise NameError(
                    "ignnspector does not currenly have a proposer sub-class "
                    "with the name provided to the 'proposer_name' argument")
        
        elif not isinstance(proposer_name, Proposer) or type(proposer_name) != Proposer:
            raise TypeError(
                "If a class obeject is given to the 'proposer_name' argument "
                "it has to be a Proposer sub-class object")
        
        else:
            proposer = proposer_name

        

    def compare_models(self, other_model):
        pass