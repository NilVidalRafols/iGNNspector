from ignnspector.analysis.analysis import analyse
# import sys
# sys.path.append(sys.path[0].replace('/tests/builder', ''))

import yaml
import torch
from torch_geometric.datasets import Planetoid
from torch_geometric.transforms import ToSparseTensor
import torch.nn.functional as F

from ignnspector import Graph
from ignnspector.analysis import analyse
from ignnspector.model.builders import pyg_builder
from ignnspector.model import GNN


def test_pyg_builder():
    with open('tests/proposer/report_2.yaml', 'r') as f:
        report = yaml.full_load(f)

    components = pyg_builder(report)
    model = GNN(components)
    print(model)
    return model


def train_test(model):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

    model.train()
    for epoch in range(200):
        optimizer.zero_grad()
        out = model(data)
        loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
        if epoch % 25 == 0:
            print(f'Epoch: {epoch:03d}')

    model.eval()
    _, pred = model(data).max(dim=1)
    correct = int(pred[data.test_mask].eq(data.y[data.test_mask]).sum().item())
    acc = correct / int(data.test_mask.sum())
    print('Accuracy: {:.4f}'.format(acc))


if __name__ == '__main__':


    dataset = Planetoid(root='/tmp/Cora', name='Cora')
    data = dataset[0]
    
    # analyse dataset
    graph = Graph(data)
    graph_report = analyse(data, split_size=5000, num_splits=5)

    # get proposals
    
    print(data)
    # ToSparseTensor adds to data an antribute adj_t
    edge_index = data.edge_index
    transform = ToSparseTensor()
    transform(data)
    # recover the edge_index
    data.edge_index = edge_index

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Device:', device)

    data = data.to(device)

    # test the PyG model
    PyG_model = PyG_gcn([
        ('conv1', GCNConv(dataset.num_node_features, 16)),
        ('conv2', GCNConv(16, dataset.num_classes))
        ]).to(device)
    print('\nPyG model:')
    train_test(PyG_model)


