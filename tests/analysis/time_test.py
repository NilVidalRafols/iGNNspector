# import sys
# sys_path = '/tests/analysis'
# sys.path.append(sys.path[0].replace(sys_path, ''))
import yaml

from ignnspector import Graph
from ignnspector.analysis import analyse_with_time
import torch_geometric as pyg

print('Downloading dataset')
dataset = pyg.datasets.CitationFull(name='Cora', root='D:\\tmp')
print('Initializing graph')
total_graph = Graph(dataset[0], single_representation=True)
print('Done')

times = 10, 20, 30, 40
for time in times:
    report = analyse_with_time(total_graph, time=time)

    print('time:', time)
    print('real time:', report['total_time'])
    print()
    # with open('persistence/reports/CiteSeer.yaml', 'w') as f:
    #     yaml.dump(report, f)