
import networkx as nx

def available_metrics_for(graph):
    pass

nx.degree_histogram(G)
nx.algorithms.cluster.average_clustering(G)
nx.density(G)
nx.algorithms.components.connected_components(G)
nx.algorithms.components.strongly_connected_components(G)
nx.average_shortest_path_length(cc)
nx.diameter(cc)
nx.radius(cc)
nx.algorithms.connectivity.connectivity.node_connectivity(cc)
nx.algorithms.connectivity.connectivity.edge_connectivity(cc)

metrics_map = [
    "num_nodes",
    "num_edges",
    "num_features",
    "num_classes",
    "prediction_type", # What will the model predict (graph/node pred, ...)
    "learning_method", # inductive/transductive learning
    "avg_degree",
    "diameter",
    "avg_path_length",
    "radius",
    "node_connectivity",
    "edge_connectivity",
    "avg_clustering_coef",
    "transitivity",
    "density",
    "homophily",
    "edge_cut"
    '''...'''
]