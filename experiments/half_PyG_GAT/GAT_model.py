from torch_geometric.data import Data
from torch_geometric.nn import GATConv
from torch_geometric.datasets import Planetoid
import torch_geometric.transforms as T

import matplotlib.pyplot as plt

class GAT_model(torch.nn.Module):
    def __init__(self):
        super(PyG_GAT, self).__init__()
        self.hid = 8
        self.in_head = 8
        self.out_head = 1
        
        self.conv1 = GATConv(dataset.num_features, self.hid, heads=self.in_head, dropout=0.6)
        self.conv2 = GATConv(self.hid*self.in_head, dataset.num_classes, concat=False,
                             heads=self.out_head, dropout=0.6)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        
        # Dropout before the GAT layer is used to avoid overfitting in small datasets like Cora.
        # One can skip them if the dataset is sufficiently large.
        
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv1(x, edge_index)
        x = F.elu(x)
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2(x, edge_index)
        
        return F.log_softmax(x, dim=1)

if __name__ == '__main__':
    ame_data = 'Cora'
    dataset = Planetoid(root= '/tmp/' + name_data, name = name_data)
    dataset.transform = T.NormalizeFeatures()

    print(f"Number of Classes in {name_data}:", dataset.num_classes)
    print(f"Number of Node Features in {name_data}:", dataset.num_node_features)

    print()
    model_type = input('PyG / non_PyG: ')
    