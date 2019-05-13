import re
import json

with open('data/raw/Presidential_speeches.json', 'r') as f:
    raw_corpus = json.load(f)

# president_party = {'Barack Obama': 'democrat'}
periods = [(1789, 1849), (1850, 1865), (1866, 1918), (1919, 1945),
           (1946, 1964), (1965, 1980), (1980, 1991), (1992, 2008),
           (2009, 2017)]
corpora = {}
for e in raw_corpus:
    # President X.Y. YEAR
    year = int(re.findall(r'\d{4}', e['title'])[0])
    # president = ....
    period = [p for p in periods if p[0] <= year <= p[1]][0]
    # party = president_party[president]
    cidx = periods.index(period)
    speech1 = e['speech1']
    speech2 = e['speech2']
    if cidx not in corpora.keys():
        corpora[cidx] = [speech1, speech2]
    else:
        corpora[cidx].append(speech1)
        corpora[cidx].append(speech2)

for k,v in corpora.items():
    fname = 'data/interim/%s' % str(k).zfill(2) + '.txt'
    text = [e for e in v if len(e) > 1]
    text = '\n'.join(text)
    with open(fname, 'w') as f:
        f.write(text)