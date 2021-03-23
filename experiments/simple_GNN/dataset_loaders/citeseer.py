import csv
import numpy as np


def load_citeseer():
    """
    Load the citeseer dataset
    :return: Adjacency matrix and target values. All of them in boolean matrix form.
    """
    # Load the nodes from the file
    with open('datasets/citeseer/citeseer.node_labels') as nodes_file:
        nodes_csv = csv.reader(nodes_file, delimiter=',')
        nodes = np.array([int(row[1]) for row in nodes_csv])

    # One-hot encoding
    nodes_ohe = np.zeros((len(nodes), len(np.unique(nodes))))
    for i, class_number in enumerate(nodes):
        nodes_ohe[i, class_number-1] = 1

    # Load the edges as an adjacency boolean matrix
    with open('datasets/citeseer/citeseer.edges') as edges_file:
        edges_csv = csv.reader(edges_file, delimiter=',')
        edges = np.eye(nodes.shape[0])
        for (from_idx, to_idx, _) in edges_csv:
            edges[int(from_idx)-1, int(to_idx)-1] = 1

    return edges, nodes_ohe
