from abc import ABC, abstractmethod

class Proposer(ABC):
    def __init__(self, graph=None):
        if graph != None:
            self.metrics = graph.report.contents

    @abstractmethod
    def propose_model(self, graph=None, num_proposals:int=None):
        pass

class Studies(Proposer):
    def __init__(self, graph=None):
        super(Studies, self).__init__(graph)

    def propose_model(self, graph=None, num_proposals:int=None):
        if graph != None:
            self.metrics = graph.report.contents
        
        if num_proposals == None or num_proposals < 1:
            num_proposals = 1
        # per cada mètrica de la qual sapiguem quins models responen millor,
        # existeix un condicional que afegeix el nom del model que va o
        # van millor, amb les capes necessaries.
        proposals = []

        if 'homophily' in self.metrics:
            h = float(self.metrics['homophily'])
            if h < 0.7:
                contents = {}
                contents['model_name'] = 'Geom-GCN'
                contents['num_layers'] = ['5']
                proposals.append(contents)
                contents = {}
                contents['model_name'] = 'H2GCN'
                contents['num_layers'] = ['5']
                proposals.append(contents)
            else:
                contents = {}
                contents['model_name'] = 'GCN'
                contents['num_layers'] = ['4']
                proposals.append(contents)
                contents = {}
                contents['model_name'] = 'GAT'
                contents['num_layers'] = ['4']
                proposals.append(contents)
                contents = {}
                contents['model_name'] = 'GIN'
                contents['num_layers'] = ['4']
                proposals.append(contents)

        if 'prediction_type' in self.metrics:
            pred = self.metrics['prediction_type']
            if pred == 'node':
                contents = {}
                contents['model_name'] = 'GCN'
                contents['num_layers'] = ['4']
                proposals.append(contents)
                contents = {}
                contents['model_name'] = 'GAT'
                contents['num_layers'] = ['4']
                proposals.append(contents)
                contents = {}
                contents['model_name'] = 'GCN2'
                contents['num_layers'] = ['32']
                contents['advice'] = ['Although the final model has a definite \
                    number of layers, it is adviced to try to test the model \
                    with different number of layers']
                proposals.append(contents)

            elif pred == 'graph':
                contents = {}
                contents['model_name'] = 'GCN'
                contents['num_layers'] = ['4']
                proposals.append(contents)
                contents = {}
                contents['model_name'] = 'GAT'
                contents['num_layers'] = ['4']
                proposals.append(contents)

        if 'learning_method' in self.metrics:
            m = self.metrics['learning_method']
            if m == 'transductive':
                pass
            elif m == 'inductive':
                pass

        if 'avg_clustering_coef' in self.metrics:
            c = float(self.metrics['avg_clustering_coef'])
            if c < 0.2:
                pass
        
        # features tells whath features we want to use to decide the
        # best model and how many diferent options per feature we want to
        # present
        features = [('model_name', 3),('num_layers', 1),('transform', 1)]
        proposals = self.select_best_options(proposals, features)
        
        return proposals

    def select_best_options(self, proposals, features):
        result = []
        if len(features) == 0:
            # Returns the final list of proposals without duplicates
            duplicate = lambda x,l: len([x for y in l if x == y]) > 0
            [result.append(x) for x in proposals if not duplicate(x,result)]
            return result

        feature, num_proposals = features.pop(0)
        proposals = self.count_proposals(proposals, feature)
        proposals = sorted(proposals, key=lambda x: len(x), reverse=True)
        proposals = proposals[:num_proposals]
        for group in proposals:
            result += self.select_best_options(group, features)
        return result

    # returns a list with as many lists as the number of distinct elements
    # given by the metric.
    def count_proposals(self, proposals, metric):
        key = lambda x: x[metric] if metric in x else 'none'
        proposals = sorted(proposals, key=key)
        ranking = []
        prev_value = ''
        for proposal in proposals:
            if metric in proposal and proposal[metric] != prev_value:
                    ranking.append([proposal])
                    prev_value = proposal[metric]
            elif not metric in proposal and 'none' != prev_value:
                    ranking.append([proposal])
                    prev_value = 'none'
            else:
                ranking[-1].append(proposal)
        return ranking

class DecisionTree(Proposer):
    def __init__(self, graph=None):
        super(Studies, self).__init__(graph)

    def metrics_to_model(self):
        pass
