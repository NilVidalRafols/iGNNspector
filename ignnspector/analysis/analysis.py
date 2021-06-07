
import networkx as nx
import yaml

from ignnspector.analysis.functions import *


def analyze(graph, time=None, split_size=None, num_splits=None):
    # per solucionar la questio del tems d'execucio, 
    # podria tenir la funcio entrenada i llavors, 
    # comencar amb pocs nodes i veue si la funcio dona un resultat
    # mes gran o mes petit del que volem,
    # llavors anem iterant fins que trobem un nombre de nodes optim
    split_size, num_splits = complete_parameters(graph, 
                                                 time, split_size, num_splits)

def complete_parameters(time, split_size, num_splits):
    # case 0 (None, None, None)
    # analize all the graph
    # case 1 (None, None, num_splits)
    # split_size = nodes // num_splits
    # case 2 (None, split_size, num_splits)
    # case 3 (None, split_size, None)
    # num_splits = nodes // split_size

    # case 4 (time, split_size, None)
    
    # case 5 (time, None, split_size)

    # case 6 (time, split_size, num_splits)
    return split_size, num_splits
def analyze_metrics(graph, metrics=None, split_size=None, num_splits=None):
    report = {}
    splits = graph.to_splits()

    nx_graph = graph.nx_DiGraph() if graph.directed else graph.nx_Graph()
    # run ignnspector functions
    for function in ignnspector_functions:
        if metrics != None and not function.__name__ in metrics:
            continue
        report[function.__name__] = function()
    # run networkx functions
    functions = [
            nx.algorithms.cluster.average_clustering,
    nx.density,

    ]

    for function in 

def available_metrics_for(graph):
    pass

nx.degree_histogram(G)
nx.algorithms.cluster.average_clustering(G)
nx.density(G)
nx.algorithms.components.connected_components(G)
nx.algorithms.components.strongly_connected_components(G)
nx.average_shortest_path_length(cc)
nx.diameter(cc)
nx.radius(cc)
nx.algorithms.connectivity.connectivity.node_connectivity(cc)
nx.algorithms.connectivity.connectivity.edge_connectivity(cc)

metrics_map = [
    "num_nodes",
    "num_edges",
    "num_features",
    "num_classes",
    "prediction_type", # What will the model predict (graph/node pred, ...)
    "learning_method", # inductive/transductive learning
    "avg_degree",
    "diameter",
    "avg_path_length",
    "radius",
    "node_connectivity",
    "edge_connectivity",
    "avg_clustering_coef",
    "transitivity",
    "density",
    "homophily",
    "edge_cut"
    '''...'''
]