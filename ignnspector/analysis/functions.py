import networkx as nx
import torch_geometric as pyg
from ignnspector.data import Graph

# Define some custom functions
def real_avg_degree(split, full_graph):
    if full_graph.directed:
        nx_graph = full_graph.nx_DiGraph()
        nx_split = split.nx_DiGraph()
    else:
        nx_graph = full_graph.nx_Graph()
        nx_split = split.nx_Graph()
    nodes = nx_split.nodes
    real_degree_sequence = sorted([d for n, d in nx_graph.degree(nodes)])
    real_avg_degree = sum(real_degree_sequence) / len(nodes)
    return real_avg_degree

def false_avg_degree(split):
    if split.directed:
        nx_split = split.nx_DiGraph()
    else:
        nx_split = split.nx_Graph()

    degree_sequence = sorted([d for n, d in nx_split.degree()])
    avg_degree = sum(degree_sequence) / nx_split.number_of_nodes()
    return avg_degree

def edge_cut(split, full_graph):
    if full_graph.directed:
        nx_graph = full_graph.nx_DiGraph()
        nx_split = split.nx_DiGraph()
    else:
        nx_graph = full_graph.nx_Graph()
        nx_split = split.nx_Graph()
    nodes = nx_split.nodes
    edge_cut = 0
    for n in nodes:
        rd = nx_graph.degree(n)
        d = nx_split.degree(n)
        edge_cut += rd - d
    return edge_cut

ignnspector_functions = {
    # Parameters: graph (split), full graph
    real_avg_degree,
    false_avg_degree,
    edge_cut
}

nx_functions = [
    # Parameters: graph
    nx.algorithms.cluster.average_clustering,
    nx.density,
    # Parameters: fully connected graph
    nx.average_shortest_path_length,
    nx.diameter,
    nx.radius,
    nx.algorithms.connectivity.connectivity.node_connectivity,
    nx.algorithms.connectivity.connectivity.edge_connectivity,
    # Parameters: graph, attribute name
    nx.attribute_assortativity_coefficient
]
pyg_functions = [
    # Parameters: edge_index, y
    pyg.utils.homophily_ratio
]
