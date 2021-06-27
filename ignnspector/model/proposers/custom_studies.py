import yaml

path = 'ignnspector/model/proposers/default_proposal_tree.yaml'
with open(path, 'r') as f:
    contents = yaml.full_load(f)
    
default_proposal_tree = contents

path = 'ignnspector/model/proposers/default_model_components.yaml'
with open(path, 'r') as f:
    contents = yaml.full_load(f)
    
default_model_components = contents

operators = {
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y, 
    '<': lambda x, y: x < y, 
    '>': lambda x, y: x > y, 
    '<=': lambda x, y: x <= y, 
    '>=': lambda x, y: x >= y, 
    'all': lambda x, y: True
}


def custom_studies( analysis_report, 
                    features=[('model_type', 4)], 
                    proposal_tree=default_proposal_tree):

    proposals = get_proposals(analysis_report, proposal_tree)
    proposals = select_proposals(proposals, features)

    reports = [get_report(proposal, analysis_report) for proposal in proposals]
    return reports


def get_proposals(report, proposal_tree):
    root_node = ('_', proposal_tree)
    proposals = traverse_tree(root_node, report)
    return proposals


def get_operation_value(key):
    op = key.split()[0]
    if op == 'all':
        return op, '_'
    else:
        x = key.split()[1]

    if x.isnumeric():
        return op, int(x)
    try:
        tmp_x = float(x)
    except ValueError:
        tmp_x = x
    finally:
        return op, tmp_x


def get_analysis_value(report, metric):
    if isinstance(report[metric], dict):
        return report[metric]['value']
    else:
        return report[metric]


def traverse_tree(node, report, metric=None):
    key, children = node

    # determine the type of node, it can be a 'metric' or 'condition' node
    if key.split()[0] in operators.keys():
        # It is a 'condition' node if the key contains an operator 
        # at the beginning
        op, value = get_operation_value(key)
        # check if the analysis report value satisfies the condition

        analysis_value = get_analysis_value(report, metric)
        if operators[op](analysis_value, value):
            if isinstance(children, list):
                # if the node is a 'leaf' containing a bunch of proposals,
                # return them
                return children
            else:
                # if children is another map continue traversing 
                proposals = []
                for child in children.items():
                    proposals += traverse_tree(child, report)
                return proposals
        else:
            return []
    elif key in report.keys() or key == '_':
        # It is a 'metric' node present in the analysis report or it is the root_node
        proposals = []
        for child in children.items():
            proposals += traverse_tree(child, report, key)
        return proposals
    else:
        return []


def select_proposals(proposals, features):
    result = []
    if len(features) == 0:
        # Returns the final list of proposals without duplicates
        duplicate = lambda x,l: len([x for y in l if x == y]) > 0
        [result.append(x) for x in proposals if not duplicate(x,result)]
        return result

    feature, num_proposals = features.pop(0)
    proposals = count_proposals(proposals, feature)
    proposals = sorted(proposals, key=lambda x: len(x), reverse=True)
    proposals = proposals[:num_proposals]
    for group in proposals:
        result += select_proposals(group, features)
    return result

# returns a list with as many lists as the number of distinct elements
# given by the metric.
def count_proposals(proposals, metric):
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

def get_report(proposal, analysis):
    default = default_model_components
    p = proposal
    contents = {}
    contents['model_name'] = 'iGNNspector_' + p['model_type']
    contents['model_type'] = p['model_type']

    if 'transform' in p:
        contents['transform'] = p['transform']
    if 'task' in p:
        contents['task'] = p['task']
    if 'training_mode' in p:
        contents['training_mode'] = p['training_mode']

    layers = get_layers(p, analysis, default)

    contents['layers'] = layers
    return contents

def get_layers(p, analysis, default):
    num_layers = int(p['num_layers'])
    layers = []
    
    # hidden_channels have a length equal to 20% of the input channels 
    # plus the output_channels
    hidden_channels = int(analysis['in_features'] * 0.2) + analysis['out_features']
    # add as many layers as specified in 'num_layers'
    for i in range(num_layers):
        if i == 0:
            layers.append({
                'type': p['model_type'],
                'in_features': analysis['in_features'],
                'out_features': hidden_channels,
                'activation': default['activation'],
                'dropout': default['dropout']
            })
        elif i ==  num_layers - 1:
            if analysis['task'] == 'node_classification':
                layer_type = default['layers']['last_node_clas'][0]['type']
                activ = default['layers']['last_node_clas'][0]['activation']
                layers.append({
                'type': layer_type,
                'in_features': hidden_channels,
                'out_features': analysis['out_features'],
                'activation': activ,
                'dropout': default['dropout']
                })
        else:
            layers.append({
                'type': p['model_type'],
                'in_features': hidden_channels,
                'out_features': hidden_channels,
                'activation': default['activation'],
                'dropout': default['dropout']
            })

    return layers

# def get_layers(p, default):
#     layers = []
#     # the number of hidden channels decreases at each layer by these amount
#     less_channels = analysis['in_features'] - analysis['out_features']
#     less_channels //= num_layers

#     hidden_channels = analysis['in_features']
#     # add as many layers as specified in 'num_layers'
#     for i in range(num_layers):
#         if i != num_layers - 1:
#             layers.append({
#                 'type': p['model_type'],
#                 'in_features': hidden_channels,
#                 'out_features': hidden_channels - less_channels,
#                 'activation': default['activation'],
#                 'dropout': default['dropout']
#             })
#             hidden_channels -= less_channels
#         else:
#             # add the last layer or layers according to the prediction type
#             # last_layers = []
#             if analysis['task'] == 'node_classification':
#                 layer_type = default['layers']['last_node_clas'][0]['type']
#                 activ = default['layers']['last_node_clas'][0]['activation']
#                 layers.append({
#                 'type': layer_type,
#                 'in_features': hidden_channels,
#                 'out_features': hidden_channels - less_channels,
#                 'activation': activ,
#                 'dropout': default['dropout']
#                 })
#                 # last_layers.extend(default['layers']['last_node_clas'])
#                 # last_layers[0].update({
#                 # 'in_features': hidden_channels,
#                 # 'out_features': analysis['out_features']
#                 # })

#             # elif analysis['task'] == 'graph_classification':
#             #     last_layers.extend(default['layers']['last_graph_clas'])
#             #     for layer in last_layers:
#             #         layer.update({
#             #             'in_features': hidden_channels,
#             #             'out_features': analysis['out_features']
#             #     })

#             # layers.extend(last_layers)
#     return layers