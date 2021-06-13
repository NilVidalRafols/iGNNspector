from abc import ABC, abstractmethod

class Proposer(ABC):
    def __init__(self, report=None):
        self.report = report

    @abstractmethod
    def propose_model(self, graph=None, num_proposals:int=None):
        pass


class DecisionTree(Proposer):
    def __init__(self, graph=None):
        super(Studies, self).__init__(graph)

    def metrics_to_model(self):
        pass
