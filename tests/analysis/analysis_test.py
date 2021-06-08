import sys
sys.path.append(sys.path.append('d:\\UNI\\iGNNspector'))

import yaml

from ignnspector.data import Graph
from ignnspector.analysis import analyze
import torch_geometric as pyg

dataset = pyg.datasets.CitationFull(name='CiteSeer', root='/tmp')
total_graph = Graph(dataset[0], single_representation=False)

report = analyze(total_graph, split_size=2000)

with open('tests/analysis/analysis.yaml', 'w') as f:
    yaml.dump(report)