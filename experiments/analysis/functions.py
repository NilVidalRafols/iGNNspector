import networkx as nx
import torch_geometric as pyg
from ignnspector.data import Graph


# Define some custom functions
def real_avg_degree(split, G, to_nx):
    nodes = to_nx(split).nodes
    if split.directed:
        nx_G = G.nx_DiGraph()
    else:
        nx_G = G.nx_Graph()
    real_degree_sequence = sorted([d for n, d in nx_G.degree(nodes)])
    real_avg_degree = sum(real_degree_sequence) / len(nodes)
    return real_avg_degree

def false_avg_degree(nx_split):
    degree_sequence = sorted([d for n, d in nx_split.degree()])
    avg_degree = sum(degree_sequence) / nx_split.number_of_nodes()
    return avg_degree

def edge_cut(split, G, to_nx):
    nx_split = to_nx(split)
    nodes = nx_split.nodes
    if split.directed:
        nx_G = G.nx_DiGraph()
    else:
        nx_G = G.nx_Graph()
    edge_cut = 0
    for n in nodes:
        rd = nx_G.degree(n)
        d = nx_split.degree(n)
        edge_cut += rd - d
    return edge_cut

# Group the functions that will be used acording to what parameters they use
functions_split = [
    false_avg_degree,
    nx.algorithms.cluster.average_clustering,
    nx.density,
]
functions_cc = [
    nx.average_shortest_path_length,
    nx.diameter,
    nx.radius,
    nx.algorithms.connectivity.connectivity.node_connectivity,
    nx.algorithms.connectivity.connectivity.edge_connectivity
]
functions_split_G = [
    real_avg_degree,
    edge_cut
]
