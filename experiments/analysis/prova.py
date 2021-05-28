import ogb.nodeproppred as ogbn

dataset = ogbn.NodePropPredDataset(name='ogbn-products', root='/tmp')
thing = dataset[0]
print(type(thing))
print(thing)
print(dataset[0][0]['node_feat'])
print(dataset[0][0]['num_nodes'])

# try to split the graph
