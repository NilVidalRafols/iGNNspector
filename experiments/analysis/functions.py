import networkx as nx
import torch_geometric as pyg


# Define some custom functions
def real_avg_degree(split, G):
    nodes = split.nx_DiGraph().nodes
    nx_G = G.nx_DiGraph()
    real_degree_sequence = sorted([d for n, d in nx_G.degree(nodes)])
    real_avg_degree = sum(real_degree_sequence) / len(nodes)
    return real_avg_degree

def false_avg_degree(nx_split):
    degree_sequence = sorted([d for n, d in nx_split.degree()])
    avg_degree = sum(degree_sequence) / split.num_nodes
    return avg_degree

def edge_cut(split, G):
    nx_split = split.nx_DiGraph()
    nodes = nx_split.nodes
    nx_G = G.nx_DiGraph()
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

functions = [
    (false_avg_degree, ['graph']),
    (nx.algorithms.cluster.average_clustering, ['graph']),
    (nx.density, ['graph']),
    (nx.average_shortest_path_length, ['biggest_cc']),
    (nx.diameter, ['biggest_cc']),
    (nx.radius, ['biggest_cc']),
    (nx.algorithms.connectivity.connectivity.node_connectivity, ['biggest_cc']),
    (nx.algorithms.connectivity.connectivity.edge_connectivity, ['biggest_cc']),
    (real_avg_degree, ['graph', 'total_graph']),
    (edge_cut, ['graph', 'total_graph'])
]

def run():
    pass