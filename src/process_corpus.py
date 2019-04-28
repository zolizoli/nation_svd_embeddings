import spacy
from os import listdir
from os.path import isfile, join

in_path = 'data/interim'
out_path = 'data/processed'
nlp = spacy.load("en_core_web_sm")

corpora = [f for f in listdir(in_path) if isfile(join(in_path, f))]
bad_pos = ['PUNCT', 'SYM', 'X', 'NUM', 'SPACE']
for corpus in corpora:
    with open(join(in_path, corpus), 'r') as f:
        txts = f.read().strip().split('\n')
        processed = []
        for txt in txts:
            new_text = txt[:]
            raw_doc = nlp(txt)
            for entity in raw_doc.ents:
                if ' ' in entity.text:
                    connected = entity.text.replace(' ', '|')
                    new_text = new_text[:entity.start_char] + connected + new_text[entity.end_char:]
            doc = nlp(new_text)
            for token in doc:
                if token.pos_ not in bad_pos:
                    t = token.lemma_.lower()
                    if t != '-pron-':
                        processed.append(t)
        with open(join(out_path, corpus), 'w') as of:
            of.write(' '.join(processed))
