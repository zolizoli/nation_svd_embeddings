import json
import re

import nltk


with open('data/raw/Presidential_speeches.json', 'r') as f:
    json_file = json.load(f)

with open('data/nation/todie.tsv', 'w') as outfile:
    h = 'Sentence ID\tSentence\tSpeech ID\tPresident\tTitle\n'
    outfile.write(h)
    i = 0
    for element in json_file:
        president = element['president']
        speech1 = element['speech1']
        speech2 = element['speech2']
        fid = element['id']
        title = element['title']
        speeches = ''
        if len(speech1) > 1:
            speeches += speech1
        if len(speech2) > 1:
            speeches += ' ' + speech2
        speeches = speeches.replace('\t', ' ')
        speeches = speeches.replace('&nbsp;', '')
        sent_text = nltk.sent_tokenize(speeches)
        for sentence in sent_text:
            tokenized_text = nltk.word_tokenize(sentence)
            checked_text = [wd.lower() for wd in tokenized_text]
            if 'nation' in checked_text:
                o = str(i).zfill(4) + '\t' + ' '.join(tokenized_text) + '\t' + fid + '\t' + president + '\t' + title + '\n'
                outfile.write(o)
                i += 1
