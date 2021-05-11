from networkx.classes.function import to_undirected
from ignnspector.analysis.reports import GraphReport

import
import networkx as nx
import torch_geometric as pyg

class Graph:
    def __init__(self, data):
        # OGB
        self._ogb = None
        # NetworkX
        self._nx_Graph = None
        self._nx_DiGraph = None
        # PyG
        self._data = None
        self._dataset = None
        self._data = data

    def nx_Graph(self):
        if self._nx_Graph == None:
            d = self._data
            if isinstance(self._data, pyg.data.Data):
                G = pyg.utils.to_networkx(d, d.x, to_undirected=True)
            elif isinstance(self._data, tuple):
                num_nodes = d[0]['num_nodes']
                edge_index = d[0]['edge_index']
                edge_list = []
                for i in range(len(edge_index[0])):
                    v = int(edge_index[0][i])
                    u = int(edge_index[1][i])
                    edge_list.append((v, u))
                G = nx.Graph()
                G.add_nodes_from(list(range(0, num_nodes)))
                G.add_edges_from(edge_list)

            self._nx_Graph = G

        return self._nx_Graph

    def nx_DiGraph(self):
        if self._nx_DiGraph == None:
            d = self._data
            if isinstance(self._data, pyg.data.Data):
                G = pyg.utils.to_networkx(d, d.x, to_undirected=False)
            elif isinstance(self._data, tuple):
                num_nodes = d[0]['num_nodes']
                edge_index = d[0]['edge_index']
                edge_list = []
                for i in range(len(edge_index[0])):
                    v = int(edge_index[0][i])
                    u = int(edge_index[1][i])
                    edge_list.append((v, u))
                G = nx.Graph()
                G.add_nodes_from(list(range(0, num_nodes)))
                G.add_edges_from(edge_list)

            self._nx_DiGraph = G

        return self._nx_DiGraph

    def PyG(self):
        if self._PyG == None:
            d = self._data
            if isinstance(self._data, nx.Graph):
                G = pyg.utils.from_networkx(d)
            if isinstance(self._data, nx.DiGraph):
                G = pyg.utils.from_networkx(d)
            elif isinstance(self._data, tuple):
                edge_index = d[0]['edge_index']
                is_undirected = pyg.utils.is_undirected(edge_index)
                if is_undirected:
                    G = pyg.utils.from_networkx(self.nx_Graph())
                else:
                    G = pyg.utils.from_networkx(self.nx_DiGraph)
            self._PyG = G

        return self._PyG

    def OGB(self):
        if self._PyG == None:
            if isinstance(self._data, nx.Graph):
                pass
            if isinstance(self._data, nx.DiGraph):
                pass
            if isinstance(self._data, pyg.data.Data):
                pass

        return self._PyG

    def to_splits(self, num_splits, mode='random'):
        pass
