import csv
import os
import sys
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

# Define some custom functions
def real_avg_degree(split, G):
    nodes = to_nx(split).nodes
    nx_G = G.nx_DiGraph()
    real_degree_sequence = sorted([d for n, d in nx_G.degree(nodes)])
    real_avg_degree = sum(real_degree_sequence) / len(nodes)
    return real_avg_degree

def false_avg_degree(nx_split):
    degree_sequence = sorted([d for n, d in nx_split.degree()])
    avg_degree = sum(degree_sequence) / split.num_nodes
    return avg_degree

def edge_cut(split, G):
    nx_split = to_nx(split)
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

if pyg.utils.is_undirected(total_graph.PyG().edge_index):
    to_nx = lambda g: g.nx_Graph()
else:
    to_nx = lambda g: g.nx_DiGraph()

print('type finded')

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

    # Run all experiments
    i = 0
    max_split = settings['max_split'] if 'max_split' in settings else num_splits
    while i < max_split:
        split = next(splits)
        time_results['num_edges'] = split.num_edges
        # initialize nx and PyG representations
        to_nx(split)
        # Progress
        print(num_nodes, 'nodes:', end=' ')
        print('Split', i + 1, 'from', max_split, 'completed')

        # parameters: split
        for function in functions_split:
            ini_time = time.time()
            value = function(to_nx(split))
            duration = time.time() - ini_time
            time_results[function.__name__] += duration/num_splits
            value_results[function.__name__] += value/num_splits
        
        # parameters: connected_component, (biggest)
        nx_cc_func = nx.algorithms.components.strongly_connected_components
        CCs = sorted(nx_cc_func(split.nx_DiGraph()), key=len, reverse=True)
        CCs = [to_nx(split).subgraph(c).copy() for c in CCs]
        biggest_cc = CCs[0]
        for function in functions_cc:
            ini_time = time.time()
            value = function(biggest_cc)
            duration = time.time() - ini_time
            time_results[function.__name__] += duration/num_splits
            value_results[function.__name__] += value/num_splits


        # parameters: split, total graph
        for function in functions_split_G:
            ini_time = time.time()
            value = function(split, total_graph)
            duration = time.time() - ini_time
            time_results[function.__name__] += duration/num_splits
            value_results[function.__name__] += value/num_splits

        # parameters: biggest_cc, y
        ini_time = time.time()
        function = nx.attribute_assortativity_coefficient
        value = function(to_nx(split), 'y')
        duration = time.time() - ini_time
        time_results[function.__name__] += duration/num_splits
        value_results[function.__name__] += value/num_splits

        # parameters: edge_index, y
        split.PyG()
        ini_time = time.time()
        function = pyg.utils.homophily_ratio
        value = function(split.PyG().edge_index, split.PyG().y)
        duration = time.time() - ini_time
        time_results[function.__name__] += duration/num_splits
        value_results[function.__name__] += value/num_splits

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
    out_path = settings['output_path'] + dataset_name + '_times.csv'
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
    out_path = settings['output_path'] + dataset_name + '_values.csv'
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