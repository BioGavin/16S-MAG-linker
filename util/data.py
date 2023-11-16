import json


class BlastData:
    def __init__(self, dataseg):
        self.queryId, self.subId, self.identity, self.alignLen, self.mismatches, self.gapOpens, self.qStart, self.qEnd, self.sStart, self.sEnd, self.evalue, self.bitScore = dataseg


def blastReader(path):
    with open(path, 'r') as f:
        blastData = f.readlines()
    return blastData


if __name__ == '__main__':
    path = 'out.txt'
    data = blastReader(path)

    matchData = []

    for line in data:
        b = BlastData(line.split())
        if float(b.identity) >= 95 and int(b.alignLen) >= 400:
            matchData.append([b.subId, b.identity, b.alignLen])

    matchData.sort(key=lambda x: float(x[1]), reverse=True)

    print(matchData)

    with open('map.json', 'r') as f:
        mapDic = json.load(f)

    with open('dataset.json', 'r') as f:
        dataset = json.load(f)

    with open('matchPaths.txt', 'w') as f:
        for match in matchData:
            genomes = mapDic[match[0]]
            for genome in genomes:
                key = genome.split('.')[0]
                if key in dataset:
                    path = dataset[key]
                    f.write(path.replace('\\', '/') + '\n')
