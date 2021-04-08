




class Proposer:
    def __init__(self, graph=None):
        if graph != None:
            self.metrics = graph.report.metrics

    def propose_model(self, graph=None, num_proposals:int):
        if graph != None:
            self.metrics = graph.report.metrics
        
        if num_proposals == None or num_proposals < 1:
            num_proposals = 1

        self.reports = metrics_to_model(num_proposals)
        return self.reports

    def metrics_to_model(self):
        pass


class Studies(Proposer):
    def __init__(self, graph=None):
        super(Studies, self).__init__(graph)

    def metrics_to_model(self, num_proposals:int):
        # per cada mètrica de la qual sapiguem quins models responen millor,
        # existeix un condicional que afegeix el nom del model que va o
        # van millor, i les capes necessaries.
        transforms = []
        models = []
        num_layers = []
        # mirar una manera de que el transform de la proposta sigui cooerent
        # amb el model de la proposta i el numero de capes, potser tenint una
        # unica llista de propostes on cada element és
        # [trasform,model,num_capes]
        if 'homophily' in self.metrics:
            h = metrics['homophily']
            if h < 0.7:
                models.append(['Geom-GCN', 'H2GCN'])
            else:
                models.append(['GCN', 'GAT', 'GIN'])

        if 'prediction_type' in self.metrics:
            pred = metrics['prediction_type']
            if pred == 'node':
                models.append(['GCN2', 'GEN'])

        if 'learning_method' in self.metrics:
            m = metrics['learning_method']
            if m == 'transductive':
                models.append(['GCN', 'GEN', 'GAT'])
            elif m == 'inductive':
                models.append(['GAT'])


        if 'avg_clustering_coef' in self.metrics:
            c = self.metrics['avg_clustering_coef']
            if c < 0.2:
                transforms.append('PCGCN') 
                num_layers.append
            

class DecisionTree(Proposer):
    def __init__(self, graph=None):
        super(Studies, self).__init__(graph)

    def metrics_to_model(self):
        pass
