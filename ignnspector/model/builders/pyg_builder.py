from torch.nn import Sequential, Linear, ReLU
from torch.nn import functional as F
from torch_geometric.nn import conv

from ignnspector.model import GNN


def get_GCNConv(layer):
    in_features = layer['in_features']
    out_features = layer['out_features']
    return conv.GCNConv(in_features, out_features)

def get_GATConv(layer):
    in_features = layer['in_features']
    out_features = layer['out_features']
    return conv.GATConv(in_features, out_features, dropout=0.5)

def get_GINConv(layer):
    in_features = layer['in_features']
    out_features = layer['out_features']
    mid_features = (in_features + out_features) // 2

    neural_network = Sequential(Linear(in_features, mid_features), 
                                ReLU(), 
                                Linear(mid_features, out_features), 
                                ReLU())

    return conv.GATConv(neural_network)

def get_GCN2Conv(layer):
    hidden_channels = layer['in_features']
    out_features = layer['out_features']
    alpha = 0.1
    theta = 0.5

    layer_conv = conv.GCN2Conv(hidden_channels, alpha, theta, layer + 1,)
    # since the GCN2Conv output has the same length than the input,
    # add a linear transformation to change the output length if needed
    if hidden_channels != out_features:
        linear = Linear(hidden_channels, out_features)
        def GCN2ConvLinear(x, x_0, edge_index):
            x = layer_conv(x, x_0, edge_index)
            return linear(x)
        return GCN2ConvLinear
    else:
        return layer_conv

def get_MLP(layer):
    in_features = layer['in_features']
    out_features = layer['out_features']
    return Linear(in_features, out_features)


layer_map = {
    'GCN': get_GCNConv,
    'GAT': get_GATConv,
    'GIN': get_GINConv,
    'GCN2': get_GCN2Conv,
    'MLP': get_MLP
}

activation_map = {
    'relu': F.relu,
    'log_softmax': F.log_softmax
}

def pyg_builder(report):
    layers = []
    dropouts = []
    activations = []
    for l in report['layers']:
        # layer convolutions
        layer_conv = layer_map[l['type']]
        layer = layer_conv(l)
        layers.append(layer)
        # dropouts
        if 'dropout' in l.keys() and l['dropout'] > 0.0:
            dropouts.append(F.dropout)
        else:
            dropouts.append(lambda x: x)
        # activations
        if 'activation' in l.keys():
            activations.append(activation_map[l['activation']])
        else:
            activations.append(lambda x: x)

    components = []
    zipped_components = zip(range(len(layers)), layers, dropouts, activations)
    for i, layer, dropout, activation in zipped_components:
        components.append({
            'name': 'conv' + str(i),
            'layer': layer, 
            'dropout': dropout, 
            'activation': activation
        })

    return components