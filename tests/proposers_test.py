import sys
sys.path.append(sys.path[0].replace('/tests', ''))

from ignnspector.analysis.reports import GraphReport
from ignnspector.data import Graph
from ignnspector.analysis import Analyzer
from ignnspector.analysis.proposers import *

def test_Studies(features):
    with open('tests/graph_report.yaml', 'r') as f:
        report_string = f.read()
    
    report = GraphReport(report_string)
    p = Studies()
    proposals = p.propose_model(report,features)
    print('done!')

test_Studies([('model_type', 1),('num_layers', 2)])
test_Studies([('model_type', 3),('num_layers', 1)])
test_Studies([('model_type', 4),('num_layers', 2)])