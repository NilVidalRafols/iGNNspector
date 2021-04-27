import sys
sys.path.append(sys.path[0].replace('/tests', ''))

from ignnspector.analysis.reports import ModelReport

import pytest

# MODEL REPORT TEST
def test_load_yaml():
    with open('tests/model_report.yaml', 'r') as f:
        report_string = f.read()
    report = ModelReport(report_string)
    print('done!')

test_load_yaml()