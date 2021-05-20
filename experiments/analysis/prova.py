import ogb.nodeproppred as ogbn

dataset = ogbn.NodePropPredDataset(name='ogbn-arxiv', root='/tmp')
thing = dataset[0][1]
print(type(thing))
print(thing)
print(dataset[0][0]['node_feat'])
print(dataset[0][0]['num_nodes'])