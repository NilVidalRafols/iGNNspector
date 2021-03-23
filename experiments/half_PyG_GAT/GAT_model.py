import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(2020) # seed for reproducible numbers

from torch_geometric.data import Data
from torch_geometric.nn import GATConv
from torch_geometric.datasets import Planetoid
import torch_geometric.transforms as T
import torch
import matplotlib.pyplot as plt

from GAT_layer import GATLayer 

class PyG_GAT(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super(PyG_GAT, self).__init__()
        self.hid = 8
        self.in_head = 8
        self.out_head = 1
        
        self.conv1 = GATConv(num_features, self.hid, heads=self.in_head, dropout=0.6)
        self.conv2 = GATConv(self.hid*self.in_head, num_classes, concat=False,
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

class non_PyG_GAT(torch.nn.Module):
    def __init__(self, num_features, num_classes):
        super(non_PyG_GAT, self).__init__()
        self.hid = 8
        self.in_head = 8
        self.out_head = 1
        
        self.conv1 = GATLayer(num_features, self.hid, dropout=0.6)
        self.conv2 = GATLayer(self.hid*self.in_head, num_classes, concat=False, dropout=0.6)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        
        # Dropout before the GAT layer is used to avoid overfitting in small datasets like Cora.
        # One can skip them if the dataset is sufficiently large.
        
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv1.forward(x, edge_index)
        x = F.elu(x)
        x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2.forward(x, edge_index)
        
        return F.log_softmax(x, dim=1)

