import torch

from gnn.gcn import GraphConvolutionalNetwork, GraphConvolutionalLayer
from dataset_loaders import load_cora, load_citeseer, random_graph, load_blogcatalog, load_mutag, load_twitch

import torch.cuda.profiler as profiler
import pyprof2
pyprof2.init()


def dense_to_sparse(dense_matrix):
    indices = torch.nonzero(dense_matrix).t()
    values = dense_matrix[indices[0], indices[1]]
    return torch.sparse.FloatTensor(indices, values, dense_matrix.size())

def experiment_cora():
    adj, x, target = load_cora()
    adj = torch.from_numpy(adj).float().cuda()
    x = torch.from_numpy(x).float().cuda()
    target = torch.from_numpy(target).float().cuda()

    gcn = GraphConvolutionalNetwork(
        GraphConvolutionalLayer(x.shape[1], 16),
        GraphConvolutionalLayer(16, target.shape[1])
    ).cuda()
    return gcn, (adj, x)


def experiment_twitch():
    adj, x, target = load_twitch()
    adj = torch.from_numpy(adj).float().cuda()
    x = torch.from_numpy(x).float().cuda()
    target = torch.from_numpy(target).float().cuda()

    gcn = GraphConvolutionalNetwork(
        GraphConvolutionalLayer(x.shape[1], 16),
        GraphConvolutionalLayer(16, target.shape[1])
    ).cuda()
    return gcn, (adj, x)


def experiment_random_graph(n_nodes, n_attributes, n_outputs, sparsity):
    adj, x, target = random_graph(n_nodes, n_attributes, n_outputs, sparsity)
    adj = torch.from_numpy(adj).float().cuda()
    x = torch.from_numpy(x).float().cuda()
    target = torch.from_numpy(target).float().cuda()

    gcn = GraphConvolutionalNetwork(
        GraphConvolutionalLayer(x.shape[1], 16, left_to_right=False),
        GraphConvolutionalLayer(16, target.shape[1], left_to_right=False)
    ).cuda()
    return gcn, (adj, x)


def experiment_citeseer():
    adj, target = load_citeseer()
    adj = torch.from_numpy(adj).float().cuda()
    target = torch.from_numpy(target).float().cuda()

    gcn = GraphConvolutionalNetwork(
        GraphConvolutionalLayer(target.shape[1], 16),
        GraphConvolutionalLayer(16, target.shape[1])
    ).cuda()
    return gcn, (adj, target)


def experiment_mutag():
    adj, target = load_mutag()[179]
    adj = torch.from_numpy(adj).float().cuda()
    target = torch.from_numpy(target).float().cuda()

    gcn = GraphConvolutionalNetwork(
        GraphConvolutionalLayer(target.shape[1], 16),
        GraphConvolutionalLayer(16, target.shape[1])
    ).cuda()
    return gcn, (adj, target)


def experiment_blogcatalog():
    adj, target = load_blogcatalog()
    adj = torch.from_numpy(adj).float().cuda()
    target = torch.from_numpy(target).float().cuda()

    gcn = GraphConvolutionalNetwork(
        GraphConvolutionalLayer(target.shape[1], 16),
        GraphConvolutionalLayer(16, target.shape[1])
    ).cuda()
    return gcn, (adj, target)


if __name__ == '__main__':
    network, inputs = experiment_random_graph(10000, 20, 10, sparsity=0.9999)

    with torch.autograd.profiler.emit_nvtx():
        profiler.start()
        network(inputs)
        profiler.stop()