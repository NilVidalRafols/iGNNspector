import torch
from torch.nn.modules.linear import Linear
import torch_geometric

# Fix modules with https://discuss.pytorch.org/t/nn-with-configurable-number-of-layers/5202
class GNN(torch.nn.Module):
    def __init__(self, components):
        super(GNN, self).__init__()
        self.components = components
        # a name list will be necessary to retrieve the corresponding steps
        self.names = list(map(lambda c: c['name'], components))
        for name, layer in map(lambda c: (c['name'], c['layer']), components):
            self.add_module(name, layer)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        
        for name, layer in self.named_children():
            i = self.names.index(name)
            component = self.components[i]
            dropout, p = component['dropout']
            activation = component['activation']
            
            x = dropout(x, p)
            if isinstance(layer, Linear):
                x = layer(x)
            else:
                x = layer(x, edge_index)
            x = activation(x)

        return x



# class PyG_gcn(torch.nn.Module):
#     def __init__(self, layers):
#         super(PyG_gcn, self).__init__()
#         for layer in layers:
#             self.add_module(layer[0], layer[1])
        
#     def forward(self, data):
#         x, edge_index = data.x, data.edge_index

#         layers = list(self.named_children())
#         for _, layer in layers:
#             x = layer(x, edge_index)
#             if layer != layers[-1]:
#                 x = torch.nn.functional.relu(x)
#                 x = torch.nn.functional.dropout(x, training=self.training)

#         return torch.nn.functional.log_softmax(x, dim=1)

# class PyG_GAT(torch.nn.Module):
#     def __init__(self, num_features, num_classes):
#         super(PyG_GAT, self).__init__()
#         self.hid = 8
#         self.in_head = 8
#         self.out_head = 1
        
#         self.conv1 = GATConv(num_features, self.hid, heads=self.in_head, dropout=0.6)
#         self.conv2 = GATConv(self.hid*self.in_head, num_classes, concat=False,
#                              heads=self.out_head, dropout=0.6)

#     def forward(self, data):
#         x, edge_index = data.x, data.edge_index
        
#         # Dropout before the GAT layer is used to avoid overfitting in small datasets like Cora.
#         # One can skip them if the dataset is sufficiently large.
        
#         x = F.dropout(x, p=0.6, training=self.training)
#         x = self.conv1(x, edge_index)
#         x = F.elu(x)
#         x = F.dropout(x, p=0.6, training=self.training)
#         x = self.conv2(x, edge_index)
        
#         return F.log_softmax(x, dim=1)
