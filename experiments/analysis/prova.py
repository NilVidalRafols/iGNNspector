import sys
sys_path = '/experiments/analysis'
sys.path.append(sys.path[0].replace(sys_path, ''))

import ogb.nodeproppred as ogbn
from ignnspector.data import Graph

dataset = ogbn.NodePropPredDataset(name='ogbn-proteins', root='/tmp')
thing = dataset[0]
print(type(thing))
print(thing)
print(dataset[0][0]['node_feat'])
print(dataset[0][0]['num_nodes'])

# try to convert to nx graph
G = Graph(thing)
pyg_G = G.PyG()
print('pyg done')
subgraph = G.subgraph(num_nodes=500)
print('subgraph done')