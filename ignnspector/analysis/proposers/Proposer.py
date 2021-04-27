from abc import ABC, abstractmethod

class Proposer(ABC):
    def __init__(self, graph=None):
        if graph != None:
            self.metrics = graph.report.contents

    @abstractmethod
    def propose_model(self, graph=None, num_proposals:int=None):
        pass


class DecisionTree(Proposer):
    def __init__(self, graph=None):
        super(Studies, self).__init__(graph)

    def metrics_to_model(self):
        pass
