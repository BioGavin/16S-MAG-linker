import subprocess
import json
import os
from tqdm import tqdm
from threading import Thread, Lock


class BlastData:
    def __init__(self, dataseg):
        self.queryId, self.subId, self.identity, self.alignLen, self.mismatches, self.gapOpens, self.qStart, self.qEnd, self.sStart, self.sEnd, self.evalue, self.bitScore = dataseg


class ANIData:
    def __init__(self, dataseg):
        self.query, self.ref, self.ani, self.match, self.total = dataseg


def create_key(dic, key, value):
    if key in dic:
        dic[key].append(value)
    else:
        dic[key] = [value]


def get_filelist(dir, Filelist):
    newDir = dir

    if os.path.isfile(dir):

        Filelist.append(dir)

        # # 若只是要返回文件文，使用这个

        # Filelist.append(os.path.basename(dir))

    elif os.path.isdir(dir):

        for s in os.listdir(dir):
            # 如果需要忽略某些文件夹，使用以下代码

            # if s == "xxx":

            # continue

            newDir = os.path.join(dir, s)

            get_filelist(newDir, Filelist)

    return Filelist


def excuteCommand(com):
    devNull = open(os.devnull, 'w')
    ex = subprocess.Popen(com, stdout=devNull, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    # print("cmd in:", com)
    # print("cmd out: ", out.decode())
    # return out.decode()


def makedb(dbname):
    input_data = 'makeblastdb -in %s -dbtype nucl -out ref -parse_seqids' % (dbname)
    print('Start making database...it may take a few minutes...')
    excuteCommand(input_data)
    print("Database complete.")


def blast_16S(fna):
    input_data = 'blastn -query "%s" -db reference/ref -out blastResult.txt -outfmt 6 -evalue 1e-5' % (fna)
    print('Start blast analysis...it may take a few minutes...')
    excuteCommand(input_data)
    print('complete.')


def blast_reader(path):
    with open(path, 'r') as f:
        blastData = f.readlines()
    return blastData


def blast_filter(path):
    print('Filter Blast result...')
    data = blast_reader(path)

    matchData = {}
    matchDic = {}

    for line in data:
        b = BlastData(line.split())
        if float(b.identity) >= 99.0 and int(b.alignLen) >= 400:
            if b.queryId not in matchData:
                create_key(matchData, b.queryId, [b.subId, b.identity, b.alignLen])

    # matchData.sort(key=lambda x:float(x[1]), reverse=True)

    # print(matchData)

    with open('map.json', 'r') as f:
        mapDic = json.load(f)

    with open('dataset.json', 'r') as f:
        dataset = json.load(f)

    with open('matchdic.json', 'w') as f:
        for match in matchData:
            for refseq in matchData[match]:
                genomes = mapDic[refseq[0]]
                identity = float(refseq[1])
                for genome in genomes:
                    key = genome.split('.')[0]
                    if key in dataset:
                        path = dataset[key]
                        create_key(matchDic, match, [path.replace('\\', '/'), identity])

        json.dump(matchDic, f)

    print('Complete')


def ani_compare(query, matchName, out):
    # input_data = 'fastANI --ql %s --rl %s -o %s > /dev/null 2>&1' % (query, matchName, out)
    input_data = 'fastANI --ql %s --rl %s -o %s' % (query, matchName, out)
    excuteCommand(input_data)


def ani_getinfo(path, dic_16s, dic_mag, name_16s, identity_16S):
    with open(path, 'r') as f:
        data = f.readlines()

    aniDic = {}
    matchmag = []

    for ani in data:
        aniInfo = ANIData(ani.split())

        if aniInfo.query not in aniDic:
            aniDic[aniInfo.query] = [aniInfo.ani, aniInfo.match, aniInfo.total]
        else:
            if aniInfo.ani > aniDic[aniInfo.query][0]:
                aniDic[aniInfo.query] = [aniInfo.ani, aniInfo.match, aniInfo.total]

    for i in aniDic:
        if float(aniDic[i][0]) >= 95 and i not in matchmag:
            create_key(dic_16s, name_16s, [i, aniDic[i][0], identity_16S, aniDic[i][1], aniDic[i][2]])
            create_key(dic_mag, i, [name_16s, aniDic[i][0], identity_16S, aniDic[i][1], aniDic[i][2]])
            matchmag.append(i)

    if not matchmag and aniDic:
        max_ani = 0
        max_i = ''
        for i in aniDic:
            if float(aniDic[i][0]) > max_ani:
                max_ani = float(aniDic[i][0])
                max_i = i
        create_key(dic_16s, name_16s, [max_i, aniDic[max_i][0], identity_16S, aniDic[max_i][1], aniDic[max_i][2]])


def genome_match(dic_16s, dic_mag, match, matchDic, diclock):
    max_identity = -1

    count = 0

    with open('./matchData/' + 'matchPaths_%s.txt' % (match), 'w') as f:
        for path, identity in matchDic[match]:
            count += 1

            f.write(path + '\n')

            if identity > max_identity:
                max_identity = identity

            if count >= 10:
                break

    if os.path.getsize('./matchData/' + 'matchPaths_%s.txt' % (match)) != 0:
        ani_name = './resultData/' + '%s_16s.txt' % (match)
        ani_compare('magspath.txt', './matchData/' + 'matchPaths_%s.txt' % (match), ani_name)

        diclock.acquire()
        ani_getinfo(ani_name, dic_16s, dic_mag, match, max_identity)
        diclock.release()

    # print(dic_16s)
