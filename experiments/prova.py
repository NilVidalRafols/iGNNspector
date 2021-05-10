import sys
sys.path.append(sys.path[0].replace('/experiments', ''))

from ignnspector.analysis.reports import GraphReport,ModelReport
from ignnspector.analysis.proposers import Studies

import yaml


with open('tests/graph_report.yaml') as f:
    contents = yaml.safe_load(f)

graph_report = GraphReport(contents=contents)

proposer = Studies(graph_report)

features = [
    ('model_type', 4),
    ('num_layers', 2),
    ('transform', 1)
]

proposals = proposer.propose_model(features=features)

for proposal in proposals:
    with open('experiments/' + proposal.contents['model_name'] + '.yaml', 'w') as f:
        f.write(proposal.yaml_string())
