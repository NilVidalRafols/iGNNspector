import numpy as np


def random_graph(n_nodes, n_attributes, n_outputs, sparsity=0.5):
    """
    Create a random graph with a predetermined sparsity.
    :param n_nodes: Number of nodes the graph should have.
    :param n_attributes: Number of attributes that each node should have.
    :param n_outputs: Number of attributes in the output of each node.
    :param sparsity: Percentage of sparsity expected. Calculated as percentage of existing edges divided by the
    potential total edges n_nodes**2. A value of 1.0 means a totally disconnected graph, while a value of 0.0 means
    a fully connected graph.
    :return: Adjacency matrix (n_nodes * n_nodes), attributes of the nodes (n_nodes * n_attributes) and target
    values (n_nodes * n_outputs).
    """
    adj = np.random.rand(n_nodes, n_nodes)
    for i in range(0, adj.shape[0]):
        for j in range(0, adj.shape[1]):
            adj[i, j] = 1.0 if adj[i, j] > sparsity else 0.0
    x = np.random.rand(n_nodes, n_attributes)
    target = np.random.rand(n_nodes, n_outputs)
    return adj, x, target
