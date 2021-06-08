
from networkx.algorithms.components import connected_components
from networkx.algorithms.components import strongly_connected_components
import yaml
import time as t

from ignnspector.analysis.functions import *
from ignnspector.data import Graph

def analyze(graph, time=None, split_size=None, num_splits=None):
    if time != None:
        report = analyze_with_time(graph, time, split_size, num_splits)
        return report

    # get splits to analyze and correct values 
    # from split_size and num_splits if needed
    splits, split_size, num_splits = get_splits(graph, split_size, num_splits)

    # the characterization of the graph is saved in a dict
    report = init_report(graph, split_size, num_splits)

    nx = lambda g: g.nx_DiGraph() if g.directed else g.nx_Graph()
    for  split, i in zip(splits, range(num_splits)):
        nx(split)
        # run ignnspector metrics
        for function, j in zip(ignnspector_functions, range(len(nx_functions))):
            if j < 1:
                ini_time = t.time()
                value = function(split)
                duration = t.time() - ini_time
            else:
                ini_time = t.time()
                value = function(split, graph)
                duration = t.time() - ini_time
            report[function.__name__]['value'] += value / num_splits
            report[function.__name__]['time'] += duration / num_splits

        # run networkx metrics
        split_cc = biggest_connected_component(nx(split))
        for function, j in zip(nx_functions, range(len(nx_functions))):
            if j < 2:
                ini_time = t.time()
                value = function(nx(split))
                duration = t.time() - ini_time
            elif j < 7:
                ini_time = t.time()
                value = function(split_cc)
                duration = t.time() - ini_time
            else:
                ini_time = t.time()
                value = function(nx(split), 'y')
                duration = t.time() - ini_time
            report[function.__name__]['value'] += value / num_splits
            report[function.__name__]['time'] += duration / num_splits

        # run torch_geometric metrics
        split.PyG()
        for function in pyg_functions:
            ini_time = t.time()
            try:
                value = function(split.PyG().edge_index, split.PyG().y)
            except Exception:
                value = 0
            duration = t.time() - ini_time
            report[function.__name__]['value'] += value / num_splits
            report[function.__name__]['time'] += duration / num_splits
    
    return report

def get_splits(graph, split_size, num_splits):
    if split_size == None and num_splits == None:
        num_splits = 1
        splits = [graph]
    elif split_size == None:
        split_size = graph.num_nodes // num_splits
        splits = graph.to_splits(split_size)
    elif num_splits == None:
        num_splits = graph.num_nodes // split_size
        splits = graph.to_splits(split_size)
    else:
        splits = graph.to_splits(split_size)
        num_splits = min(graph.num_nodes // split_size, num_splits)

    return splits, split_size, num_splits

def init_report(graph, split_size, num_splits):
    report = {
        'num_nodes': graph.num_nodes,
        'num_edges': graph.num_edges,
        'split_size': split_size,
        'num_splits': num_splits,
    }
    for key in ignnspector_functions:
        report[key.__name__] = {'value':0.0, 'time':0.0}
    for key in nx_functions:
        report[key.__name__] = {'value':0.0, 'time':0.0}
    for key in pyg_functions:
        report[key.__name__] = {'value':0.0, 'time':0.0}
    return report

def biggest_connected_component(graph):
    if graph.is_directed():
        ccs = strongly_connected_components(graph)
        bcc = sorted(ccs, key=len, reverse=True)[0]
    else:
        ccs = connected_components(graph)
        ccs = sorted(ccs, key=len, reverse=True)
        bcc = sorted(ccs, key=len, reverse=True)[0]

    biggest_connected_component = graph.subgraph(bcc).copy()
    return biggest_connected_component

def analyze_with_time(graph, time, split_size=None, num_splits=None):
    pass

# metrics_map = [
#     "num_nodes",
#     "num_edges",
#     "num_features",
#     "num_classes",
#     "prediction_type", # What will the model predict (graph/node pred, ...)
#     "learning_method", # inductive/transductive learning
#     "avg_degree",
#     "diameter",
#     "avg_path_length",
#     "radius",
#     "node_connectivity",
#     "edge_connectivity",
#     "avg_clustering_coef",
#     "transitivity",
#     "density",
#     "homophily",
#     "edge_cut"
#     '''...'''
# ]