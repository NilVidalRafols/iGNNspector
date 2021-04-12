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
        # van millor, i les capes necessaries.
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
                contents['num_layers'] = '4'
                proposals.append(contents)
                contents = {}
                contents['model_name'] = 'GAT'
                contents['num_layers'] = '4'
                proposals.append(contents)
                contents['model_name'] = 'GCN2'
                contents['num_layers'] = ['16','32','64']
                contents['advice'] = ['Although the final model has a definite \
                    number of layers, it is adviced to try to test the model \
                    with different number of layers']
                proposals.append(contents)
            elif pred == 'graph':
                contents = {}
                contents['model_name'] = 'GCN'
                contents['num_layers'] = '4'
                proposals.append(contents)
                contents = {}
                contents['model_name'] = 'GAT'
                contents['num_layers'] = '4'
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
        
        models = self.select_best_models(proposals, num_proposals)
        
        return models
            
    def select_best_models(self, proposals, num_proposals):
        models = sorted(proposals, key=lambda x: x['model_name'])
        return models


class DecisionTree(Proposer):
    def __init__(self, graph=None):
        super(Studies, self).__init__(graph)

    def metrics_to_model(self):
        pass
