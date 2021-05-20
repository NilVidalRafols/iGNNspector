import csv
import os
import sys
from unittest import result

from tqdm import tqdm
import yaml
sys_path = '/experiments/analysis/ogbn-arxiv'
sys.path.append(sys.path[0].replace(sys_path, ''))

import ogb.nodeproppred as ogbn
import networkx as nx
import torch_geometric as pyg
from ignnspector.data import Graph
import time

# Get settings from yaml file
with open('/experiments/analysis/settings.yaml', 'r') as f:
    settings = yaml.full_load(f)

inc_rate = float(settings['node_increment'][:-1]) / 100
if settings['node_increment'][-1] == '%':
    node_increment = lambda num_nodes: int(num_nodes * (1 + inc_rate))
else:
    node_increment = lambda num_nodes: num_nodes + inc_rate

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


# Create Graph and splits
dataset = ogbn.NodePropPredDataset(name='ogbn-arxiv', root='/tmp')
G = Graph(dataset[0])
to_splits = G.to_splits(NUM_NODES)

# Remove the last split since it could contain less nodes than NUM_NODES
splits = list(to_splits)[:-1]

# Set the dict that will store the results
results = {}
results.update({key.__name__: 0.0 for key in functions_split})
results.update({key.__name__: 0.0 for key in functions_cc})
results.update({key.__name__: 0.0 for key in functions_split_G})
results['attribute_assortativity_coefficient'] = 0.0
results['homophily(method=edge)'] = 0.0
results['homophily(method=node)'] = 0.0


# Run all experiments
while True:
    for split in splits:
        # Progress
        index = splits.index(split) + 1
        print('Split', index, 'from', len(splits), 'completed')

        # parameters: split
        for function in functions_split:
            ini_time = time.time()
            function(split.nx_DiGraph())
            duration = time.time() - ini_time
            results[function.__name__] += duration/len(splits)
        
        # parameters: connected_component, (biggest)
        nx_cc_func = nx.algorithms.components.strongly_connected_components
        CCs = sorted(nx_cc_func(split.nx_DiGraph()), key=len, reverse=True)
        CCs = [split.nx_DiGraph().subgraph(c).copy() for c in CCs]
        cc = CCs[0]
        for function in functions_cc:
            ini_time = time.time()
            function(cc)
            duration = time.time() - ini_time
            results[function.__name__] += duration/len(splits)

        # parameters: split, total graph
        for function in functions_split_G:
            ini_time = time.time()
            function(split, G)
            duration = time.time() - ini_time
            results[function.__name__] += duration/len(splits)

        # parameters: cc, y
        ini_time = time.time()
        function = nx.attribute_assortativity_coefficient
        function(split.nx_DiGraph(), 'y')
        duration = time.time() - ini_time
        results[function.__name__] += duration/len(splits)

        # parameters: edge_index, y
        ini_time = time.time()
        function = pyg.utils.homophily
        function(split.PyG().edge_index, 'y', method='edge')
        duration = time.time() - ini_time
        results[function.__name__+'(method=edge)'] += duration/len(splits)

        ini_time = time.time()
        function = pyg.utils.homophily
        function(split.PyG().edge_index, 'y', method='edge')
        duration = time.time() - ini_time
        results[function.__name__+'(method=node)'] += duration/len(splits)

# write the results in a csv file
path = sys_path + 'ogbn-arxiv_' + str(NUM_NODES) + '.csv'
with open(path, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['function', 'time'])
    for key, value in results.items():
        w.writerow([key,value])

# if os.path.exists(path):
#     with open(path, 'a', newline='') as f:
#         w = csv.DictWriter(f, results.keys())
#         w.writerow(results)

# else:
#     with open(path, 'w', newline='') as f:
#         w = csv.DictWriter(f, results.keys())
#         w.writeheader()
#         w.writerow(results)