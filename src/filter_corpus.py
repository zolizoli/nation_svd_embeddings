from os import listdir
from os.path import isfile, join
from collections import Counter

in_path = 'data/processed'
out_path = 'data/filtered'

with open('data/stopwords.txt', 'r') as f:
    stopwords = f.read().strip().split('\n')

txts = [f for f in listdir(in_path) if isfile(join(in_path, f))]

vocabs = []
for txt in txts:
    with open(join(in_path, txt), 'r') as f:
        wds = Counter(f.read().split())
        vocabs.append(set(wds.keys()))
shared_vocabulary = set.intersection(*vocabs)
shared_vocabulary = {wd for wd in shared_vocabulary if wd not in stopwords
                     and len(wd) > 2}
for txt in txts:
    with open(join(in_path, txt), 'r') as f:
        wds = Counter(f.read().split())
        wds = [wd for wd in wds if wd not in stopwords and len(wd) > 2]
        wds = ' '.join(wds)
        with open(join(out_path, txt.split('.')[0], txt), 'w') as of:
            of.write(wds)
