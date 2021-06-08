import sys
sys_path = '/experiments/analysis'
sys.path.append(sys.path[0].replace(sys_path, ''))

import pickle
import torch_geometric as pyg

from ignnspector.analysis import Graph


dataset = pyg.datasets.Planetoid(name='CiteSeer', root='/tmp')
graph = Graph(dataset[0])

with open('CiteSeer.pickle', 'wb') as f:
    pickle.dump(graph.nx_DiGraph())