import os
import sys
sys_path = '/experiments/analysis'
# sys.path.append(sys.path[0].replace(sys_path, ''))
sys.path.append(sys.path.append('d:\\UNI\\iGNNspector'))

import pickle
from torch_geometric.datasets import Planetoid

from ignnspector.analysis import Graph


dataset = Planetoid(name='CiteSeer', root=os.getcwd())
graph = Graph(dataset[0])

with open('CiteSeer.pickle', 'wb') as f:
    pickle.dump('graph.nx_DiGraph()', f)