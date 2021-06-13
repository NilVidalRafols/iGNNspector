import sys
sys.path.append(sys.path[0].replace('/tests/proposer', ''))

from ignnspector.analysis.reports import GraphReport
from ignnspector.data import Graph
from ignnspector.analysis import Analyzer
from ignnspector.proposers import *

def test_Studies(features):
    with open('tests/graph_report.yaml', 'r') as f:
        report_string = f.read()
    
    report = GraphReport(report_string)
    p = Studies()
    proposals = p.propose_model(report,features)

    for proposal in proposals:
        print(proposal.yaml_string())
    return proposals

# test_Studies([('model_type', 1),('num_layers', 2)])
# test_Studies([('model_type', 3),('num_layers', 1)])
proposals = test_Studies([('model_type', 4),('num_layers', 2)])
for proposal, i in zip(proposals, range(len(proposals))):
    with open('tests/proposer/report_' + str(i) + '.yaml', 'w') as f:
        yaml.dump(proposal.contents, f)
