# import sys
# sys_path = '/tests/analysis'
# sys.path.append(sys.path[0].replace(sys_path, ''))
import yaml

from ignnspector import Graph
from ignnspector.analysis import analyse
import torch_geometric as pyg

print('Downloading dataset')
dataset = pyg.datasets.CitationFull(name='CiteSeer', root='D:\\tmp')
print('Initializing graph')
total_graph = Graph(dataset[0], single_representation=False)
print('Done')

report = analyse(total_graph, split_size=total_graph.num_nodes)

with open('persistence/reports/CiteSeer.yaml', 'w') as f:
    yaml.dump(report, f)