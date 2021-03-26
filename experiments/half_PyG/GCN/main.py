import torch
import torch.nn.functional as F
from torch_geometric.datasets import Planetoid
from torch_geometric.transforms import ToSparseTensor
from torch_geometric.nn import GCNConv

from gcn import PyG_gcn, simple_PyG_gcn, simple_gcn, simple_gcn_layer

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


    # test the simple model
    simple_model = simple_gcn(
        simple_gcn_layer(dataset.num_node_features, 16),
        simple_gcn_layer(16, dataset.num_features)
    ).to(device)
    print('\nSimple model:')
    train_test(simple_model)

    # test the simple and PyG model
    simple_PyG_model = simple_PyG_gcn([
        ('conv1', simple_gcn_layer(dataset.num_node_features, 16)),
        ('conv2', GCNConv(16, dataset.num_classes))
        ]).to(device)
    print('\nSimple and PyG model:')
    train_test(simple_PyG_model)


    # print(type(data.adj_t))

    # # Transfer data object to GPU.
    # device = torch.device('cuda')
    # data = data.to(device)

    # gcn = simple_gcn(
    #     simple_gcn_layer(data.x.shape[1], 16),
    #     simple_gcn_layer(16, 7)
    # ).cuda()

    # x = gcn((data.adj_t.to_dense(), data.x))
    # print(type(x))
