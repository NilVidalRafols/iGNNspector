from networkx.readwrite.graph6 import data_to_n
import ogb.nodeproppred as ogbn

dataset = ogbn.NodePropPredDataset(name='ogbn-arxiv', root='/tmp')
print(type(dataset[0][0]))
print(dataset[0][0])