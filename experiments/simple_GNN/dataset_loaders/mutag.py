import csv
import numpy as np


def load_mutag():
    """
    Load the mutag dataset
    :return: Adjacency matrix and target values. All of them in boolean matrix form.
    """
    # Load the graph labels, class labels and full adjacency matrix
    with open('datasets/mutag/MUTAG_graph_indicator.txt') as mutag_graph_indicator:
        graph_indicator = np.array([int(row[0]) for row in csv.reader(mutag_graph_indicator)])

    with open('datasets/mutag/MUTAG_node_labels.txt') as mutag_node_labels:
        node_labels = [int(row[0]) for row in csv.reader(mutag_node_labels)]
        labels = np.zeros((len(node_labels), max(node_labels)+1))
        for i, label in enumerate(node_labels):
            labels[i, node_labels[i]] = 1.0

    with open('datasets/mutag/MUTAG_A.txt') as mutag_adjacency:
        adj_csv = csv.reader(mutag_adjacency)
        adj = np.eye(len(node_labels))
        for (from_idx, to_idx) in adj_csv:
            adj[int(from_idx) - 1, int(to_idx) - 1] = 1.0

    # Split the big graph into the different subgraphs according to graph_indicator
    return [
        (adj[graph_indicator == i][:, graph_indicator == i], labels[graph_indicator == i, ])
        for i in range(min(graph_indicator), max(graph_indicator)+1)
    ]
