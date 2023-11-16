import json

with open('mag.json', 'r') as f:
    data = json.load(f)

total = 200
match = 0
avg = 0
err = 0
count = len(data)

for mag in data:
    frigr = False
    mag_name = mag.split('/')[-1]
    mag_name = '_'.join([mag_name.split('_')[0], mag_name.split('_')[1]])
    for queue in data[mag]:
        if mag_name == queue[0]:
            match += 1
            frigr = True
        avg += 1
    if not frigr:
        err += 1

print(match / total)
print(avg / count)
print(err / avg)
