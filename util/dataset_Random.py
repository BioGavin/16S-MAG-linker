import json
import random

with open('dataset.json', 'r') as f:
    dataset = json.load(f)

print(len(dataset))

new_dataset = {}

dataset_list = list(dataset)

for i in range(180000):
    key = random.choice(dataset_list)
    new_dataset[key] = dataset[key]
    dataset_list.remove(key)

with open('dataset_180000.json', 'w') as f:
    json.dump(new_dataset, f)
