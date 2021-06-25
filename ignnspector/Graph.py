from pathlib import Path
from networkx import relabel
from networkx.classes.function import to_undirected
from networkx.readwrite.gexf import read_gexf
from networkx.readwrite.gml import read_gml
from networkx.readwrite.gpickle import read_gpickle
from networkx.readwrite.graphml import read_graphml
from networkx.readwrite.nx_yaml import read_yaml
import torch
import networkx as nx
import torch_geometric as pyg
import random
import pickle

class Graph:
    def __init__(self, data=None, single_representation=False):
        if isinstance(data, Path):
            G = self.get_data_from_path(data)
        else:
            G = self.get_graph_from_data(data)

        self.__data = G
        self.__nx_Graph = None
        self.__nx_DiGraph = None
        self.__PyG = None
        self.__OGB = None
        self.single_representation = single_representation

    def get_data_from_path(self, path):
        with open(path.absolute, 'r') as f:
            if path.suffix == '.gexf':
                data = read_gexf(f)
            elif path.suffix == '.gml':
                data = read_gml(f)
            elif path.suffix == '.graphml':
                data = read_graphml(f)
            elif path.suffix == '.yaml' or path.suffix == '.yml':
                data = read_yaml(f)
            elif path.suffix == '.gpickle':
                data = read_gpickle(f)
            elif path.suffix == '.pickle':
                data = pickle.load(f)
        
        G = self.get_graph_from_data(data)
        return G

    def get_graph_from_data(self, data):
        if isinstance(data, nx.Graph) or isinstance(data, nx.DiGraph):
            #self.nodes = data.nodes
            self.num_nodes = data.number_of_nodes()
            self.num_edges = data.size()
            self.directed = True if isinstance(data, nx.DiGraph) else False
        elif isinstance(data, pyg.data.Data):
            #self.nodes = list(range(data.num_nodes))
            self.num_nodes = data.num_nodes
            self.num_edges = data.num_edges
            self.directed = not pyg.utils.is_undirected(data.edge_index)
        elif isinstance(data, tuple):
            self.num_nodes = data[0]['num_nodes']
            self.num_edges = len(data[0]['edge_index'][0])
            edge_index = torch.LongTensor(data[0]['edge_index'])
            self.directed = not pyg.utils.is_undirected(edge_index)

        return data

    def nx_Graph(self):
        if self.__nx_Graph == None:
            data = self.__data
            if isinstance(data, nx.Graph):
                G = data
            elif isinstance(data, nx.DiGraph):
                G = data.to_undirected()
            elif isinstance(data, pyg.data.Data):
                G = pyg.utils.to_networkx(data, ['x', 'y'], to_undirected=True)
            elif isinstance(data, tuple):
                num_nodes = data[0]['num_nodes']
                edge_index = data[0]['edge_index']
                edge_list = []
                for i in range(len(edge_index[0])):
                    v = int(edge_index[0][i])
                    u = int(edge_index[1][i])
                    edge_list.append((v, u))
                G = nx.Graph()
                G.add_nodes_from(list(range(0, num_nodes)))
                G.add_edges_from(edge_list)
                # add classes
                y = data[1]
                for i, feat_dict in G.nodes(data=True):
                    feat_dict.update({'y': y[i][0]})
                # and node features
                if 'node_feat' in data[0]:
                    node_feat = data[0]['node_feat']
                    for i, feat_dict in G.nodes(data=True):
                        feat_dict.update({'x': node_feat[i]})
                
            self.__nx_Graph = G
            if self.single_representation:
                self.__nx_DiGraph = None
                self.__PyG = None
                self.__OGB = None
                self.__data = self.__nx_Graph

        return self.__nx_Graph


    def nx_DiGraph(self):
        if self.__nx_DiGraph == None:
            data = self.__data
            if isinstance(data, nx.Graph):
                G = data.to_directed()
            if isinstance(data, nx.DiGraph):
                G = data
            elif isinstance(data, pyg.data.Data):
                G = pyg.utils.to_networkx(data, ['x', 'y'], to_undirected=False)
            elif isinstance(data, tuple):
                num_nodes = data[0]['num_nodes']
                edge_index = data[0]['edge_index']
                edge_list = []
                for i in range(len(edge_index[0])):
                    v = int(edge_index[0][i])
                    u = int(edge_index[1][i])
                    edge_list.append((v, u))
                G = nx.Graph()
                G.add_nodes_from(list(range(0, num_nodes)))
                G.add_edges_from(edge_list)
                # add classes
                y = data[1]
                for i, feat_dict in G.nodes(data=True):
                    feat_dict.update({'y': y[i][0]})
                if 'node_feat' in data[0]:
                    node_feat = data[0]['node_feat']
                    for i, feat_dict in G.nodes(data=True):
                        feat_dict.update({'x': node_feat[i]})

            self.__nx_DiGraph = G
            if self.single_representation:
                self.__nx_Graph = None
                self.__PyG = None
                self.__OGB = None
                self.__data = self.__nx_DiGraph

        return self.__nx_DiGraph


    def PyG(self):
        if self.__PyG == None:
            data = self.__data
            if isinstance(data, nx.Graph):
                G = pyg.utils.from_networkx(data)
            elif isinstance(data, nx.DiGraph):
                G = pyg.utils.from_networkx(data)
            elif isinstance(data, pyg.data.Data):
                G = data
            elif isinstance(data, tuple):
                edge_index = torch.LongTensor(data[0]['edge_index'])
                x = torch.LongTensor(data[0]['node_feat'])
                y = torch.LongTensor([label[0] for label in data[1]])
                G = pyg.data.Data(x=x, y=y, edge_index=edge_index)
                # is_undirected = pyg.utils.is_undirected(edge_index)
                # if is_undirected:
                #     G = pyg.utils.from_networkx(self.nx_Graph())
                # else:
                #     G = pyg.utils.from_networkx(self.nx_DiGraph())

            self.__PyG = G
            if self.single_representation:
                self.__nx_Graph = None
                self.__nx_DiGraph = None
                self.__OGB = None
                self.__data = self.__PyG

        return self.__PyG


    def OGB(self):
        if self.__OGB == None:
            data = self.__data
            if isinstance(data, nx.Graph):
                pass
            elif isinstance(data, nx.DiGraph):
                pass
            elif isinstance(data, pyg.data.Data):
                pass
            elif isinstance(data, tuple):
                G = data

        return self.__OGB


    def to_splits(self, num_nodes):
        nodes = list(range(self.num_nodes))
        
        for i in range(0, self.num_nodes, num_nodes):
            split_nodes = nodes[i:min(i + num_nodes, self.num_nodes)]
            split = self.subgraph(split_nodes)
            yield split

    def subgraph(self, nodes=None, num_nodes=None):
        if num_nodes != None:
            nodes = list(range(self.num_nodes))
            random.shuffle(nodes)
            nodes = nodes[0:min(num_nodes, self.num_nodes)]
        
        if self.directed:
            G = self.nx_DiGraph().subgraph(nodes).copy()
        else:
            G = self.nx_Graph().subgraph(nodes).copy()
            
        return Graph(G)