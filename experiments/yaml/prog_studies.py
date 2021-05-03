import yaml

my = 'experiments/yaml/my_studies.yaml'
with open(my, 'r') as f:
    contents = yaml.full_load(f)

algo = yaml.dump(contents)
print(algo)