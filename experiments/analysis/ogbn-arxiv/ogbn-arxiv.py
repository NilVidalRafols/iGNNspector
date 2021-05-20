import csv
import os
import sys

from tqdm import tqdm
sys_path = '/experiments/analysis/ogbn-arxiv'
sys.path.append(sys.path[0].replace(sys_path, ''))

import ogb.nodeproppred as ogbn
import networkx as nx
from ignnspector.data import Graph
import time

# Set the number of nodes of the split
NUM_NODES = 10000

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

# Run all experiments
for split in splits:
    # Progress
    index = splits.index(split) + 1
    print('Split', index, 'from', len(splits), 'completed')
    for function in functions_split:
        ini_time = time.time()
        function(split.nx_DiGraph())
        duration = time.time() - ini_time
        results[function.__name__] += duration/len(splits)
    
    CC = [split.nx_DiGraph().subgraph(c).copy() for c in sorted(nx.algorithms.components.strongly_connected_components(split.nx_DiGraph()), key=len, reverse=True)]
    cc = CC[0]
    for function in functions_cc:
        ini_time = time.time()
        function(cc)
        duration = time.time() - ini_time
        results[function.__name__] += duration/len(splits)

    for function in functions_split_G:
        ini_time = time.time()
        function(split, G)
        duration = time.time() - ini_time
        results[function.__name__] += duration/len(splits)

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