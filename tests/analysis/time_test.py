import sys
sys_path = '/tests/analysis'
sys.path.append(sys.path[0].replace(sys_path, ''))
import yaml

from ignnspector import Graph
from ignnspector.analysis import analyse_with_time
import torch_geometric as pyg

dataset = pyg.datasets.CitationFull(name='Cora', root='/tmp')
total_graph = Graph(dataset[0], single_representation=False)

time = 10
report = analyse_with_time(total_graph, time=time)

all_times = []
for d in report.values():
    if isinstance(d, dict):
        all_times.append(d['time'])
real_time = sum(all_times)

print('time:', time)
print('real time:', real_time)
# with open('persistence/reports/CiteSeer.yaml', 'w') as f:
#     yaml.dump(report, f)