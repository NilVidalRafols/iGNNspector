import csv
import os
import sys
from numpy import NaN
from torch_geometric.utils import num_nodes

import yaml
sys_path = '/experiments/analysis'
sys.path.append(sys.path[0].replace(sys_path, ''))

import ogb.nodeproppred as ogbn
import ogb.linkproppred as ogbl
import networkx as nx
import torch_geometric as pyg
from ignnspector.data import Graph
import time

from experiments.analysis.functions import *

# Get settings from yaml file
settings_path = sys.argv[1]
with open(settings_path, 'r') as f:
    settings = yaml.full_load(f)

if isinstance(settings['node_increment'], str):
    inc_rate = float(settings['node_increment'][:-1]) / 100.0
    node_increment = lambda num_nodes: int(num_nodes * (1 + inc_rate))
else:
    inc_rate = settings['node_increment']
    node_increment = lambda num_nodes: num_nodes + inc_rate

# Create Graph
dataset_name = settings['dataset'][2]
single = settings['single_representation']
if settings['dataset'][0] == 'ogb':
    if settings['dataset'][1] == 'node_pred':
        dataset = ogbn.NodePropPredDataset(name=dataset_name, root='/tmp')
    elif settings['dataset'][1] == 'link_pred':
        dataset = ogbl.PygLinkPropPredDataset(name=dataset_name, root='/tmp')
    total_graph = Graph(dataset[0], single_representation=single)

elif settings['dataset'][0] == 'pyg':
    if settings['dataset'][1] == 'Planetoid':
        dataset = pyg.datasets.Planetoid(name=dataset_name, root='/tmp')
        total_graph = Graph(dataset[0], single_representation=single)

print('graph loaded')

if total_graph.directed:
    to_nx = lambda g: g.nx_Graph()
else:
    to_nx = lambda g: g.nx_DiGraph()

num_nodes = settings['initial_split_length']
while num_nodes < total_graph.num_nodes:
    # get the split generator
    splits = total_graph.to_splits(num_nodes)
    # track the possible number of splits of same length
    num_splits = total_graph.num_nodes // num_nodes
    print('generator')
    # Set the dict that will store the time_results for this split length
    time_results = {}
    time_results['num_nodes'] = num_nodes
    time_results['num_edges'] = 0
    time_results.update({key.__name__: 0.0 for key in functions_split})
    time_results.update({key.__name__: 0.0 for key in functions_cc})
    time_results.update({key.__name__: 0.0 for key in functions_split_G})
    time_results['attribute_assortativity_coefficient'] = 0.0
    time_results['homophily_ratio'] = 0.0
    time_results['total'] = 0.0
    # Set the dict that will store the value_results for this split length
    value_results = time_results.copy()
    del value_results['total']

    # Run all experiments
    i = 0
    if 'max_splits' in settings and settings['max_splits'] < num_splits:
        max_splits = settings['max_splits']
    else:
        max_splits = num_splits
    while i < max_splits:
        split = next(splits)
        time_results['num_edges'] = split.num_edges
        value_results['num_edges'] = split.num_edges
        # initialize nx and PyG representations
        to_nx(split)
        # Progress
        print(num_nodes, 'nodes:', end=' ')
        print('Split', i + 1, 'from', max_splits, 'completed')

        # parameters: split
        for function in functions_split:
            ini_time = time.time()
            value = function(to_nx(split))
            duration = time.time() - ini_time
            time_results[function.__name__] += duration/max_splits
            value_results[function.__name__] += value/max_splits
        
        # parameters: connected_component, (biggest)
        if split.directed:
            nx_cc_func = nx.algorithms.components.strongly_connected_components
            CCs = sorted(nx_cc_func(split.nx_DiGraph()), key=len, reverse=True)
        else:
            nx_cc_func = nx.algorithms.components.connected_components
            CCs = sorted(nx_cc_func(split.nx_Graph()), key=len, reverse=True)
        CCs = [to_nx(split).subgraph(c).copy() for c in CCs]
        biggest_cc = CCs[0]
        for function in functions_cc:
            ini_time = time.time()
            try:
                value = function(biggest_cc)
            except Exception:
                value = 0
            duration = time.time() - ini_time
            time_results[function.__name__] += duration/max_splits
            value_results[function.__name__] += value/max_splits


        # parameters: split, total graph
        for function in functions_split_G:
            ini_time = time.time()
            value = function(split, total_graph)
            duration = time.time() - ini_time
            time_results[function.__name__] += duration/max_splits
            value_results[function.__name__] += value/max_splits

        # parameters: biggest_cc, y
        ini_time = time.time()
        function = nx.attribute_assortativity_coefficient
        value = function(to_nx(split), 'y')
        duration = time.time() - ini_time
        time_results[function.__name__] += duration/max_splits
        value_results[function.__name__] += value/max_splits

        # parameters: edge_index, y
        split.PyG()
        function = pyg.utils.homophily_ratio
        ini_time = time.time()
        try:
            value = function(split.PyG().edge_index, split.PyG().y)
        except Exception:
            value = 0
        duration = time.time() - ini_time
        time_results[function.__name__] += duration/max_splits
        value_results[function.__name__] += value/max_splits

        i += 1
    # After compliting a split size experiment, add all functions duration
    # to save the total time
    total_time = 0.0
    for key, t in time_results.items():
        if key != 'total' and key != 'num_nodes' and key != 'num_edges':
            total_time += t
    time_results['total'] = total_time
    print('Avarage time for', num_nodes, 'nodes is', total_time, 'seconds')

    # write time_results in a csv file
    out_path = settings['output_path'] + 'times_all'
    if 'title' in settings:
        out_path += '_' + settings['title']
    out_path += '.csv'
    if os.path.exists(out_path):
        with open(out_path, 'a', newline='') as f:
            w = csv.DictWriter(f, time_results.keys())
            w.writerow(time_results)
    else:
        with open(out_path, 'w', newline='') as f:
            w = csv.DictWriter(f, time_results.keys())
            w.writeheader()
            w.writerow(time_results)

    # write value_results in a csv file
    out_path = settings['output_path'] + 'values_all'
    if 'title' in settings:
        out_path += '_' + settings['title']
    out_path += '.csv'
    if os.path.exists(out_path):
        with open(out_path, 'a', newline='') as f:
            w = csv.DictWriter(f, value_results.keys())
            w.writerow(value_results)
    else:
        with open(out_path, 'w', newline='') as f:
            w = csv.DictWriter(f, value_results.keys())
            w.writeheader()
            w.writerow(value_results)

    num_nodes = node_increment(num_nodes)

print('FINISHED!')