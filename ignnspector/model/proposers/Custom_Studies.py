from ignnspector.model.proposers import Proposer
from ignnspector.analysis.reports import ModelReport

import yaml

class CustomStudies(Proposer):
    def __init__(self, report=None):
        super(Studies, self).__init__(report)

    def propose_model(self, graph_report=None, features:list=None):
        if graph_report != None:
            metrics = graph_report.contents
        else:
            metrics = self.report.contents
        # 'features' tells what features we want to use to decide the
        # best model and how many diferent options per feature we want to
        # present
        if features == None or len(features) < 1 or len(features[0]) != 2:
            features = [('model_type', 1),('num_layers', 1),('transform', 1)]

        proposals = self.get_proposals_from(metrics)
        proposals = self.select_best_options(proposals, features)
        
        reports = [self.get_report_from(proposal,metrics)
                    for proposal in proposals]
        return reports


    def get_proposals_from(self, metrics):
        proposals = []
        if 'homophily' in metrics:
            h = float(metrics['homophily'])
            if h < 0.6:
                proposals.append({
                    'model_type': 'Geom-GCN',
                    'num_layers': '5'
                })
                proposals.append({
                    'model_type': 'H2GCN',
                    'num_layers': '5'
                })
            else:
                proposals.append({
                    'model_type': 'GCN',
                    'num_layers': '4'
                })
                proposals.append({
                    'model_type': 'GAT',
                    'num_layers': '3'
                })
                proposals.append({
                    'model_type': 'GIN',
                    'num_layers': '4',
                })

        if 'prediction_type' in metrics:
            pred = metrics['prediction_type']
            if pred == 'node_classification':
                proposals.append({
                    'model_type': 'GCN',
                    'num_layers': '4'
                })
                proposals.append({
                    'model_type': 'GAT',
                    'num_layers': '4'
                })
                proposals.append({
                    'model_type': 'GCN2',
                    'num_layers': '32',
                    'advice': ['Although the final model has a definite '
                        'number of layers, it is adviced to try to test '
                        'the model with different number of layers']
                })

            elif pred == 'graph_classification':
                proposals.append({
                    'model_type': 'GCN',
                    'num_layers': '4',
                })
                proposals.append({
                    'model_type': 'GAT',
                    'num_layers': '4',
                })
            elif pred == 'node_prediction':
                proposals.append({
                    'model_type': 'Geom-GCN',
                    'num_layers': '5'
                })
                proposals.append({
                    'model_type': 'GCN2',
                    'num_layers': '16',
                    'advice': ['Although the final model has a definite '
                        'number of layers, it is adviced to try to test '
                        'the model with different number of layers']
                })

        if 'learning_method' in metrics:
            m = metrics['learning_method']
            if m == 'transductive':
                proposals.append({
                    'model_type': 'GAT',
                    'num_layers': '4',
                })

            elif m == 'inductive':
                proposals.append({
                    'model_type': 'GCN',
                    'num_layers': '4',
                })


        if 'avg_clustering_coef' in metrics:
            c = float(metrics['avg_clustering_coef'])
            if c < 0.2:
                pass
        
        if 'modularity' in metrics:
            c = float(metrics['modularity'])
            if c < 0.5:
                proposals.append({
                    'model_type': 'GAT',
                    'num_layers': '4',
                })
            else:
                proposals.append({
                    'model_type': 'CE-GCN',
                    'num_layers': '3'
                })

        return proposals

    def select_proposals(self, features, proposals):
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
            result += self.select_proposals(features, group)
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

    def get_report_from(self, proposal, metrics):
        # Create a metrics dict and add everything according to the proposal.
        # Use the model_type and num_layers to define the layers. If something
        # required is not specified in the proposal, just add a default value.
        
        # Load the default contents for the model report
        with open('ignnspector/analysis/proposers/default.yaml', 'r') as f:
            default = yaml.safe_load(f)

        p = proposal
        contents = {}
        contents['model_name'] = 'iGNNspector_' + p['model_type']
        contents['model_type'] = p['model_type']
        num_layers = int(p['num_layers'])

        if 'transform' in p:
            contents['transform'] = p['transform']

        if 'prediction_type' in p:
            contents['prediction_type'] = p['prediction_type']
        
        if 'training_mode' in p:
            contents['training_mode'] = p['training_mode']

        layers = []
        # the number of hidden channels decreases at each layer by these amount
        less_channels = metrics['num_features'] - metrics['num_classes']
        less_channels //= num_layers

        hidden_channels = metrics['num_features']
        # add as many layers as specified in 'num_layers'
        for i in range(num_layers):
            if i != num_layers - 1:
                layers.append({
                    'type': p['model_type'],
                    'in_features': hidden_channels,
                    'out_features': hidden_channels - less_channels,
                    'activation': default['activation']
                })
                hidden_channels -= less_channels
            else:
                # add the last layer or layers according to the prediction type
                last_layers = []
                if metrics['prediction_type'] == 'node_classification':
                    last_layers.extend(default['layers']['last_node_clas'])
                    last_layers[0].update({
                    'in_features': hidden_channels,
                    'out_features': metrics['num_classes']
                    })
                elif metrics['prediction_type'] == 'graph_classification':
                    last_layers.extend(default['layers']['last_graph_clas'])
                    for layer in last_layers:
                        layer.update({
                            'in_features': hidden_channels,
                            'out_features': metrics['num_classes']
                    })
                layers.extend(last_layers)

        contents['layers'] = layers
        return ModelReport(contents=contents)