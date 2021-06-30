import sys
import torch
import yaml
import torch_geometric as pyg

from ignnspector import Graph
from ignnspector.analysis.analysis import analyse
from ignnspector.model.proposers.custom_studies import custom_studies
from ignnspector.model.builders import pyg_builder
from ignnspector.model import GNN

def get_analysis_report(name):
    path = 'D:\\tmp' if sys.platform == 'win32' else '/tmp'
    dataset = pyg.datasets.CitationFull(name=name, root=path)
    graph = Graph(dataset[0], single_representation=False)
    analysis_report = analyse(graph)
    print(analysis_report)
    analysis_report['task'] = 'node_classification'
    return analysis_report

def get_proposals(analysis_report):
    proposals = custom_studies(analysis_report)
    return proposals

def train(data, model, optimizer, criterion):
      model.train()
      optimizer.zero_grad()  # Clear gradients.
      out = model(data)  # Perform a single forward pass.
      loss = criterion(out[data.train_mask], data.y[data.train_mask])  # Compute the loss solely based on the training nodes.
      loss.backward()  # Derive gradients.
      optimizer.step()  # Update parameters based on gradients.
      return loss

def test(data, model):
      model.eval()
      out = model(data)
      pred = out.argmax(dim=1)  # Use the class with highest probability.
      test_correct = pred[data.test_mask] == data.y[data.test_mask]  # Check against ground-truth labels.
      test_acc = int(test_correct.sum()) / int(data.test_mask.sum())  # Derive ratio of correct predictions.
      return test_acc

def main():

    # analysis_report = get_analysis_report('CiteSeer')
    analysis_report = {'num_nodes': 4230, 'num_edges': 10674, 
    'split_size': 4230, 'split_num_edges': [10674], 'num_splits': 1, 
    'false_avg_degree': {'value': 2.523404255319149, 
    'time': 0.0008471012115478516}, 
    'real_avg_degree': {'value': 2.523404255319149, 'time': 0.0009729862213134766}, 
    'edge_cut': {'value': 0.0, 'time': 0.006560087203979492}, 
    'average_clustering': {'value': 0.11678134183176847, 
    'time': 0.02448296546936035}, 'density': {'value': 0.0005966905309338257, 
    'time': 0.0006880760192871094}, 
    'average_shortest_path_length': {'value': 7.419883997620464, 
    'time': 1.8703665733337402}, 'diameter': {'value': 23.0, 
    'time': 1.8333966732025146}, 'radius': {'value': 12.0, 
    'time': 1.8319025039672852}, 'node_connectivity': {'value': 1.0, 
    'time': 9.439098834991455}, 'edge_connectivity': {'value': 1.0, 
    'time': 2.458936929702759}, 
    'attribute_assortativity_coefficient': {'value': 0.9377752578717435, 
    'time': 0.0057315826416015625}, 
    'homophily': {'value': 0.5, 'time': 1.9073486328125e-06}, 
    'total_time': 17.472986221313477}
    analysis_report['task'] = 'node_classification'
    analysis_report['time_efficiency'] = 'low'
    analysis_report['in_features'] = 1433
    analysis_report['out_features'] = 7

    proposals = get_proposals(analysis_report)
    for proposal in proposals:
        print(proposal)
    models = []
    for proposal in proposals:
        components = pyg_builder(proposal)
        if components == None:
            continue
        model = GNN(components)
        models.append(model)

        #print(components)
        print(model)
        print()

    path = 'D:\\tmp' if sys.platform == 'win32' else '/tmp'
    dataset = pyg.datasets.Planetoid(name='Cora', root=path)
    data = dataset[0]
    # test models
    for model in models:
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
        criterion = torch.nn.CrossEntropyLoss()
        for epoch in range(1, 201):
            loss = train(data, model, optimizer, criterion)
            print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}')

        test_acc = test(data, model)
        print(model)
        print(f'Test Accuracy: {test_acc:.4f}')
        print()