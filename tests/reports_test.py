import sys
sys.path.append(sys.path[0].replace('/tests', ''))

from ignnspector.analysis.reports import *

import pytest

# MODEL REPORT TEST
def test_load_model_yaml():
    with open('tests/model_report.yaml', 'r') as f:
        report_string = f.read()
    report = ModelReport(report_string)
    print('done!')

test_load_model_yaml()

# GRAPH REPORT TEST
def test_load_graph_yaml():
    with open('tests/graph_report.yaml', 'r') as f:
        report_string = f.read()
    report = GraphReport(report_string)
    print('done!')

test_load_graph_yaml()
