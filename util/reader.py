import json

with open('dataset.json', 'r') as f:
    dataset = json.load(f)

print(dataset['GCF_012271835'])
