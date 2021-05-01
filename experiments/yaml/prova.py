import yaml

# with open('experiments/yaml/learnyaml-es.yaml', 'r') as f:
#     dic = yaml.full_load(f)

# dic = {
#     'primer': 'hola',
#     'segon': [
#         1,
#         2,
#         3
#     ]
# }

# with open('experiments/yaml/my.yaml', 'w') as f:
#     algo = yaml.dump(dic, f)

GCN, my = 'ignnspector/analysis/reports/premade/GCN.yaml','experiments/yaml/my.yaml'
with open(my, 'r') as f:
    contents = yaml.full_load(f)

with open(my, 'w') as f:
    yaml.dump(contents, f)
