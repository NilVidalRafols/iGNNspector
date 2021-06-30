import yaml
import torch_geometric as pyg
import torch

from ignnspector import Graph
from ignnspector.analysis import analyse
from ignnspector.model.proposers import custom_studies
from ignnspector.model.builders import pyg_builder
from ignnspector.model import GNN


def train(data, model):
    model.train()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)
    criterion = torch.nn.CrossEntropyLoss()

    for epoch in range(1, 101):
        optimizer.zero_grad()  # Clear gradients.
        out = model(data)  # Perform a single forward pass.
        loss = criterion(out[data.train_mask], data.y[data.train_mask])  # Compute the loss solely based on the training nodes.
        loss.backward()  # Derive gradients.
        optimizer.step()  # Update parameters based on gradients.
        if epoch % 50 == 0:
            print(f'Epoch: {epoch:03d} / 100, Loss: {loss:.4f}')



def test(data, model):
    model.eval()
    out = model(data)
    pred = out.argmax(dim=1)  # Use the class with highest probability.
    test_correct = pred[data.test_mask] == data.y[data.test_mask]  # Check against ground-truth labels.
    test_acc = int(test_correct.sum()) / int(data.test_mask.sum())  # Derive ratio of correct predictions.
    return test_acc


Cora_dataset = pyg.datasets.Planetoid(name='Cora', root='/tmp')[0]

#######################################
###              DEMO               ###
#######################################

# Load data into an iGNNspector graph
graph = Graph(Cora_dataset)

# analyze a split size of 750 nodes
analysis_report = analyse(graph, split_size=750)

# save the analysis report
with open('Cora.yaml', 'w') as f:
    contents = yaml.dump(analysis_report, f)

# get a list of model reports from the proposer function 
# using a simple proposal tree
with open('demo_tree.yaml', 'r') as f:
    demo_tree = yaml.full_load(f)

# to generate proposals we need to add the input and output features
# of the GNN model as well as the prediction task
analysis_report['in_features'] = 1433
analysis_report['out_features'] = 7
analysis_report['task'] = 'node_classification'
proposals = custom_studies(analysis_report, proposal_tree=demo_tree)

# save all model reports
for proposal in proposals:
    with open('demo_proposals/' + proposal['model_name'] + '.yaml', 'w') as f:
        yaml.dump(proposal, f)

# build GNN models from proposals
models = []
for proposal in proposals:
    components = pyg_builder(proposal)
    if components != None:
        model = GNN(components)
        models.append(model)

# test GNN models
for model, name in zip(models, map(lambda p: p['model_type'], proposals)):
    train(Cora_dataset, model)
    acc = test(Cora_dataset, model)
    print(name, 'model accuracy:', acc)
    print()
