import util.util as util
import json
import os
from tqdm import tqdm
from threading import Thread, Lock
import queue
import argparse
import util.output as output

parser = argparse.ArgumentParser(description='Calculate connection between 16S and MAG')

parser.add_argument('-t', '--thread', metavar='', type=int, help='Num of threads')

parser.add_argument('-r', '--rna', metavar='', type=str, help='Num of rna')

parser.add_argument('-g', '--genome', metavar='', type=str, help='Num of genome')

parser.set_defaults(thread=8)

args = parser.parse_args()


def work(q, dic_16s, dic_mag, matchDic, diclock, pbar):
    while True:
        if q.empty():
            return
        else:
            do = q.get()
            pbar.update()
            util.genome_match(dic_16s, dic_mag, do, matchDic, diclock)


folder_16s = './16s'

temp_16s = util.get_filelist(folder_16s, [])
list_16s = []

count = 0

for e in temp_16s:
    if e.endswith('.fasta') or e.endswith('.fna'):
        list_16s.append(e)
        count += 1

folder_mag = './mag'

temp_mag = util.get_filelist(folder_mag, [])

list_mag = []

Tcount = 0

for e in temp_mag:

    if e.endswith('.fna.gz') or e.endswith('.fna') or e.endswith('.fa'):
        list_mag.append(e)
        Tcount += 1

with open('magspath.txt', 'w') as f:
    for i in list_mag:
        f.write(i + '\n')

count = 0

dic_16s = {}
dic_mag = {}

diclock = Lock()

q = queue.Queue()

if not os.path.exists('./matchData'):
    os.mkdir('./matchData')

if not os.path.exists('./resultData'):
    os.mkdir('./resultData')

for seg in tqdm(list_16s):
    print(seg)
    count += 1
    print('Start %d batch of 16S rRNA analysis' % (count))
    util.blast_16S(seg)
    util.blast_filter('blastResult.txt')

    with open('matchdic.json', 'r') as f:
        matchDic = json.load(f)

    for match in matchDic:
        print(match)
        q.put(match)

    pbar = tqdm(total=len(matchDic))
    print('OK')
    thread_num = args.thread
    threads = []
    for i in range(thread_num):
        t = Thread(target=work, args=(q, dic_16s, dic_mag, matchDic, diclock, pbar))
        # args需要输出的是一个元组，如果只有一个参数，后面加，表示元组，否则会报错
        threads.append(t)
    # 创建5个线程
    for i in range(thread_num):
        threads[i].start()
    for i in range(thread_num):
        threads[i].join()

with open('16s.json', 'w') as f:
    json.dump(dic_16s, f)

with open('mag.json', 'w') as f:
    json.dump(dic_mag, f)

output.makexlsx('16s.xlsx', dic_16s, ['16S', 'MAG', 'valuation'])
output.makexlsx('mag.xlsx', dic_mag, ['MAG', '16S', 'valuation'])

print('Analysis Complete! Please check 16s.xlsx and mag.xlsx to get more infomation.')
