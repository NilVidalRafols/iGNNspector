from ignnspector.analysis.reports import GraphReport
from ignnspector.data import Graph
from ignnspector.analysis import Analyzer
from ignnspector.analysis.proposers import Studies

contents = {}
contents['name'] = 'Reddit'
contents['num_nodes'] = '24'
contents['num_edges'] = '56'

with open('tests/graph_report_file_1.txt', 'r') as f:
    report = GraphReport(f.read())
    d = report.contents
    print([k in d and d[k] == x for (k,x) in contents.items()])

graph = Graph(report)
analyzer = Analyzer(graph)
proposer = Studies(graph)

models = analyzer.propose_model_using('Studies', 3)

print(models)