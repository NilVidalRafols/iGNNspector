from ignnspector.analysis.reports import GraphReport
from ignnspector.data import Graph
from ignnspector.analysis import Analyzer
from ignnspector.analysis.proposers import Studies



    with open('tests/graph_report.yaml', 'r') as f:
        report_string = f.read()
    report = GraphReport(report_string)
    print('done!')
