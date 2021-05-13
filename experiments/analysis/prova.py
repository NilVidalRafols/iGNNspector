import ogb.nodeproppred as ogbn

dataset = ogbn.NodePropPredDataset(name='ogbn-arxiv', root='/tmp')
thing = dataset[0][0].keys()
print(type(thing))
print(thing)
print(dataset[0][0]['node_feat'])