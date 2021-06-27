import yaml

from ignnspector.model.proposers import custom_studies


path = 'persistence/reports/CiteSeer.yaml'
with open(path, 'r') as f:
    report = yaml.full_load(f)

proposals = custom_studies(report, [('model_type', 10)])

for proposal in proposals:
    model_report = yaml.dump(proposal)
    print(model_report)