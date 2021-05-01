# python imports

# external imports

# tool imports
from ignnspector.data import Graph
from ignnspector.analysis.reports import *
from ignnspector.analysis.proposers import *

class Analyzer:

    def __init__(self, graph, model=None):
        if isinstance(graph, Graph):
            self.graph = graph
        else:
            self.graph = Graph()

    def analyse_graph(self, graph=None):
        #self.graph.report = report
        pass

    # def analyse_model(self, model: ['''Model'''ModelReport]):
    #     r"""Analyze a model and writte its corresponding model report
    #     """
    #     pass
    
    def propose_model_using(self, technique=None,
                            num_proposals:int=None):
                                    
        if type(technique) == str:
            try:
                proposer = eval(technique)()
            except NameError as err:
                raise NameError(
                    "ignnspector does not currenly have a proposer sub-class "
                    "with the name provided to the 'technique' argument")
        
        elif not isinstance(technique, Proposer) or type(technique) != Proposer:
            raise TypeError(
                "If a class obeject is given to the 'technique' argument "
                "it has to be a Proposer sub-class object")
        
        else:
            proposer = technique

        self.proposals = proposer.propose_model(self.graph.report, num_proposals)
        return self.proposals

    def compare_models(self, other_model):
        pass