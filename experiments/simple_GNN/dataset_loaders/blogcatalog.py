import csv
import numpy as np


def load_blogcatalog():
    """
    Load the blogcatalog dataset
    :return: Adjacency matrix and target values. All of them in boolean matrix form.
    """
    # Load the number of nodes and groups/classes
    with open('datasets/blogcatalog/nodes.csv') as nodes_file:
        nodes_csv = csv.reader(nodes_file, delimiter=',')
        n_nodes = len([row for row in nodes_csv])
    with open('datasets/blogcatalog/groups.csv') as groups_file:
        groups_csv = csv.reader(groups_file, delimiter=',')
        n_groups = len([row for row in groups_csv])

    # Load the edges as an adjacency boolean matrix
    with open('datasets/blogcatalog/edges.csv') as edges_file:
        edges_csv = csv.reader(edges_file, delimiter=',')
        edges = np.eye(n_nodes)
        for (from_idx, to_idx) in edges_csv:
            edges[int(from_idx)-1, int(to_idx)-1] = 1

    # Load the classes of each edge
    with open('datasets/blogcatalog/group-edges.csv') as group_edges_file:
        classes_csv = csv.reader(group_edges_file, delimiter=',')
        classes = np.zeros((n_nodes, n_groups))
        for (idx, group) in classes_csv:
            classes[int(idx)-1, int(group)-1] = 1

    return edges, classes
