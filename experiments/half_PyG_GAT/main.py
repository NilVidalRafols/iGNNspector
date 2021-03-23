import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from torch_geometric.data import Data
from torch_geometric.nn import GATConv
from torch_geometric.datasets import Planetoid
import torch_geometric.transforms as T
import matplotlib.pyplot as plt

from GAT_model import PyG_GAT, non_PyG_GAT

# Download or open the dataset
name_data = 'Cora'
dataset = Planetoid(root= '/home/nvidal/tfg/iGNNspector/data/Planetoid' + name_data, name = name_data)
dataset.transform = T.NormalizeFeatures()

print(f"Number of Classes in {name_data}:", dataset.num_classes)
print(f"Number of Node Features in {name_data}:", dataset.num_node_features)

# Ask the user what version of GAT wants to use
model_type = input('PyG / non_PyG: ')
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

if model_type == 'PyG':
    model = PyG_GAT(dataset.num_features, dataset.num_classes).to(device)
elif model_type == 'non_PyG':
    model = non_PyG_GAT(dataset.num_features, dataset.num_classes).to(device)
else:
    sys.exit('Invalid model type name')

print('PyG model and dataset sent to', device)


data = dataset[0].to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.005, weight_decay=5e-4)

print('Start training')

model.train()
for epoch in range(1000):
    model.train()
    optimizer.zero_grad()
    out = model(data)
    loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
    
    if epoch%200 == 0:
        print(loss)
    
    loss.backward()
    optimizer.step()
    if epoch % 200 == 0:
        print('Epoch', epoch, 'completed')

model.eval()
_, pred = model(data).max(dim=1)
correct = float(pred[data.test_mask].eq(data.y[data.test_mask]).sum().item())
acc = correct / data.test_mask.sum().item()
print('Accuracy: {:.4f}'.format(acc))