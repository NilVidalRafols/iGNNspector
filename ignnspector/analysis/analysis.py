
from networkx.algorithms.components import connected_components
from networkx.algorithms.components import strongly_connected_components
import yaml
import time as t
import random
import numpy as np
from sklearn.linear_model import *
from sklearn.metrics import mean_squared_error, median_absolute_error
import csv
from pathlib import Path

from ignnspector.analysis.functions import *
from ignnspector.data import Graph

def analyse(graph, time=None, split_size=None, num_splits=None):
    if time != None:
        report = analyse_with_time(graph, time, split_size, num_splits)
        return report

    # get splits to analyse and correct values 
    # from split_size and num_splits if needed
    splits, split_size, num_splits = get_splits(graph, split_size, num_splits)

    # the characterization of the graph is saved in a dict
    report = init_report(graph, split_size, num_splits)

    nx = lambda g: g.nx_DiGraph() if g.directed else g.nx_Graph()
    for split, _ in zip(splits, range(num_splits)):
        report['split_num_edges'].append(split.num_edges)
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
            report[function.__name__]['value'] += float(value) / num_splits
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
        'split_num_edges': [],
        'num_splits': num_splits
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

# time in seconds
def analyse_with_time(graph, time):
    model = get_best_model(graph)
    split_size, num_splits = get_splits_with_time(graph, model, time)
    report = analyse(graph, split_size=split_size, num_splits=num_splits)

    return report

def get_best_model(graph):
    # collection of regression methods 
    # (the model which gives the best results will be used)
    models = [
        LinearRegression(), 
        Ridge(), 
        BayesianRidge(),
        LassoLars(alpha=.1),
        Lasso(alpha=0.1),
        ElasticNet()
    ]

    # train a linear regressor with 10 samples from 1% nodes to up to 10% nodes
    one_100 = graph.num_nodes // 100
    num_splits = 3
    x = []
    y = []
    # set an starting percentage to make sure the starting split has some edges, 
    # if it had 0, np.log10 woud not work
    start_percentage = one_100
    split = graph.subgraph(num_nodes=one_100)
    # if some edges apear, still ad some nodes as a save margin
    save_margin = 5
    while save_margin > 0:
        start_percentage += one_100
        split = graph.subgraph(num_nodes=start_percentage)
        if split.num_edges > 0:
            save_margin -= 1
    # 10 samples starrting from start_percentage with a 1% node increment
    final_percentage = min(graph.num_nodes, start_percentage + (10 * one_100))

    for split_size in range(start_percentage, final_percentage, one_100):
        r = analyse(graph, split_size=split_size, num_splits=num_splits)
        # prepare data to train the regression model
        # input data x consist on samples of the pair (num nodes, num edges)
        num_edges = sum(r['split_num_edges']) // len(r['split_num_edges'])
        x.append((np.log10(split_size), np.log10(num_edges)))
        # autput data y consist on the base 10 logarithm of the sum of the 
        # execution time from all metrics analysed
        all_times = []
        for d in r.values():
            if isinstance(d, dict):
                all_times.append(d['time'])
        total_time = sum(all_times)
        y.append(np.log10(total_time))

    # train models
    scores = []
    for model in models:
        model.fit(x, y)
        score = mean_squared_error(y, model.predict(x))
        scores.append((model, score))
    # get the model with the best score from (model, score) pairs
    best_model = min(scores, key=lambda x: x[1])[0]
    return best_model
# perform a binary search over the number of nodes to determine the split_size 
# needed to analyse the graph with aproximately the same duration that [time]
def get_splits_with_time(graph, model, time):
    # divide time for 3, since 3 splits will be used to avarage analysis values
    time = time / 3
    split_size, num_splits = search_split_size(graph, model, time, 
                                                        0, 
                                                        graph.num_nodes)
    return split_size, num_splits

def search_split_size(graph, model, time, left, right, 
                        num_splits=3, 
                        time_range=30):
    if right >= left:
        # predict the execution time with the current split size
        split_size = left + (right - left) // 2
        splits = graph.to_splits(split_size)
        pred_time = 0.0
        for split, _ in zip(splits, range(num_splits)):
            x = [(np.log10(split.num_nodes), np.log10(split.num_edges))]
            prediction = list(map(lambda y_i: pow(10, y_i), model.predict(x)))
            pred_time += prediction[0] / num_splits

        # if the predicted time falls inside the accepted range, 
        # return the split generator, the split size and the number of splits
        if pred_time >= time - time_range / 2 \
            and pred_time <= time + time_range / 2:
            return split_size, num_splits

        elif pred_time < time - time_range / 2:
            return search_split_size(graph, model, time, 
                                    split_size + 1, 
                                    right, 
                                    num_splits, 
                                    time_range)
        else:
            return search_split_size(graph, model, time, 
                                    left, 
                                    split_size - 1, 
                                    num_splits, 
                                    time_range)
    else:
        return left, num_splits


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