from ignnspector.analysis.analysis import analyse
import sys
# sys_path = '/tests/analysis'
# sys.path.append(sys.path[0].replace(sys_path, ''))
import yaml

from ignnspector import Graph
from ignnspector.analysis import analyse_with_time
import torch_geometric as pyg

print('Downloading dataset')
path = 'D:\\tmp' if sys.platform == 'win32' else '/tmp'
dataset = pyg.datasets.CitationFull(name='PubMed', root=path)
print('Initializing graph')
total_graph = Graph(dataset[0], single_representation=False)
print('Done')

times = 60, 120
for time in times:
    report = analyse_with_time(total_graph, time=time)

    print('time:', time)
    print('real time:', report['total_time'])
    print()
    # with open('persistence/reports/CiteSeer.yaml', 'w') as f:
    #     yaml.dump(report, f)

print('full graph:', analyse(total_graph)['total_time'])