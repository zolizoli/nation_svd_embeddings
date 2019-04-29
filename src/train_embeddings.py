from os import listdir
from os.path import isdir, join

import src.svd_algebra

in_path = 'data/filtered'
out_path = 'models'

corpus = [d for d in listdir(in_path) if isdir(join(in_path, d))]
for corpora in corpus:
    try:
        a = src.svd_algebra.SVDAlgebra(join(in_path, corpora))
        a.save_model(corpora, join(out_path, corpora))
    except Exception as e:
        print('problem', e)
