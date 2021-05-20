import sys
sys.path.append(sys.path[0].replace('/tests', ''))

from ignnspector.data import Graph

import pytest
import networkx as nx
from matplotlib import pyplot as plt
import torch_geometric as pyg
import torch
import ogb.nodeproppred as ogbn

import random


def nx_graph():
    G = nx.Graph()
    G.add_nodes_from(range(5))
    G.add_edges_from([(1, 2), (1, 3), (3, 4) ,(2, 4)])
    attrs = {i: {'x': 5 - i} for i in range(G.number_of_nodes())}
    nx.classes.function.set_node_attributes(G,attrs)


    # plt.figure()
    # nx.draw(G)
    # plt.savefig('mini_graph.png')
    return G


def pyg_graph():
    edge_index = torch.tensor([
        [1, 1, 2, 2, 3, 3, 4, 4],
        [2, 3, 1, 4, 1, 4, 2, 3]
        ], dtype=torch.long)
    x = torch.tensor([[5],[4],[3],[2],[1]], dtype=torch.float)
    G = pyg.data.Data(x=x, edge_index=edge_index)
    return G


def test_Graph_types():
    nx_g = nx_graph()
    g = Graph(nx_g)
    print(g.nx_Graph().edges)
    print(g.nx_Graph().nodes(data=True))
    print(g.PyG())

    g = Graph(pyg_graph())
    print(g.nx_Graph().edges)
    print(g.nx_Graph().nodes(data=True))
    print(g.PyG())

    g = Graph(g.nx_Graph())
    print(g.nx_Graph().edges)
    print(g.nx_Graph().nodes(data=True))
    print(g.PyG())

    g = Graph(g.PyG())
    print(g.nx_Graph().edges)
    print(g.nx_Graph().nodes(data=True))
    print(g.PyG())



def test_subbgraph():
    g = Graph(nx_graph())
    g_nodes = list(range(g.num_nodes))
    random.shuffle(g_nodes)
    s_nodes = g_nodes[:3]
    s = g.subgraph(s_nodes)
    print(s.nx_Graph().edges)
    print(s.nx_Graph().nodes(data=True))

    g = Graph(pyg_graph())
    g_nodes = list(range(g.num_nodes))
    random.shuffle(g_nodes)
    s_nodes = g_nodes[:3]
    s = g.subgraph(s_nodes)
    print(s.nx_Graph().edges)
    print(s.nx_Graph().nodes(data=True))

    dataset = ogbn.NodePropPredDataset(name='ogbn-arxiv', root='/tmp')
    g = Graph(dataset[0])
    g_nodes = list(range(g.num_nodes))
    random.shuffle(g_nodes)
    s_nodes = g_nodes[:10]
    s = g.subgraph(s_nodes)
    print(s.nx_Graph().edges)
    print(s.nx_Graph().nodes(data=True))
    print(s.PyG().edge_index)
    print(s.PyG().x)



def test_to_splits():
    g = Graph(nx_graph())
    splits = list(g.to_splits(num_nodes=2))
    print(splits)
    for split in splits:
        print(split.nx_Graph().edges)
        print(split.nx_Graph().nodes(data=True))


# test_Graph_types()
# test_subbgraph()
test_to_splits()
