import pandas as pd
import json

data = pd.read_excel('../PSMPA_database.xlsx')

mapDic = {}

for i in range(len(data)):
    print(i)
    name = data.loc[i, "assembly_accession"]
    id = data.loc[i, "16S_id"]
    if id in mapDic:
        mapDic[id].append(name)
    else:
        mapDic[id] = [name]

with open('map.json', 'w') as f:
    json.dump(mapDic, f)
