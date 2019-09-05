from os import listdir
from os.path import isdir, join

import numpy as np
from scipy.stats import pearsonr, spearmanr
from scipy.spatial import procrustes
from scipy.spatial.distance import cosine
from sklearn.neighbors import NearestNeighbors

from src.svd_algebra import *


def cosine_similarity(a,b):
    t = 1 - cosine(a, b)
    if t < 0.0:
        return 0.0
    elif t > 1.0:
        return 1.0
    else:
        return t


periods = [(1789, 1849), (1850, 1865), (1866, 1918), (1919, 1945),
           (1946, 1964), (1965, 1980), (1980, 1991), (1992, 2008),
           (2009, 2017)]

in_path = 'models'

models = [d for d in listdir(in_path) if isdir(join(in_path, d))]
models.sort()

# get common vocabulary

vocabs = []
loaded_models = []
for model in models:
    a = SVDAlgebra(join(in_path, model))
    vocabs.append(set(a.vocabulary))
    loaded_models.append(a)
common_vocab = set.intersection(*vocabs)
sorted_vocab = sorted(common_vocab)


wd_shifts = {}
for wd in sorted_vocab:
    if wd not in wd_shifts.keys():
        wd_shifts[wd] = []
    initial = NearestNeighbors(n_neighbors=100, algorithm='ball_tree').fit(loaded_models[0].U)
    initial_neighbors = initial.kneighbors(loaded_models[0].U[loaded_models[0].vocabulary.index(wd)].reshape(1, -1))
    final = NearestNeighbors(n_neighbors=100, algorithm='ball_tree').fit(loaded_models[-1].U)
    final_neighbors = final.kneighbors(loaded_models[-1].U[loaded_models[-1].vocabulary.index(wd)].reshape(1, -1))
    initial_neighbors = initial_neighbors[1].tolist()[0][1:]
    final_neighbors = final_neighbors[1].tolist()[0][1:]
    initial_words = [loaded_models[0].vocabulary[j] for j in initial_neighbors
                     if loaded_models[0].vocabulary[j] in common_vocab][:5]
    final_words = [loaded_models[-1].vocabulary[j] for j in final_neighbors
                   if loaded_models[-1].vocabulary[j] in common_vocab][:5]
    print(len(final_words), len(initial_words))
    for model in loaded_models:
        period = loaded_models.index(model)
        wdidx = model.vocabulary.index(wd)

        for e in initial_words:
            iw = model.vocabulary.index(e)
            sim = cosine_similarity(model.U[wdidx], model.U[iw])
            t = ('initial', period, e, sim)
            wd_shifts[wd].append(t)
        for e in final_words:
            iw = model.vocabulary.index(e)
            sim = cosine_similarity(model.U[wdidx], model.U[iw])
            t = ('final', period, e, sim)
            wd_shifts[wd].append(t)

# strong > 0.4
# 0.4 > moderate > 0.2
# weak < 0.2
for wd, results in wd_shifts.items():
    initial_results = [e[3] for e in results if e[0] == 'initial']
    final_results = [e[3] for e in results if e[0] == 'final']
    pearson = pearsonr(initial_results, final_results)
    spearman = spearmanr(initial_results, final_results)
    if pearson[0] > 0.2 or pearson[0] < -0.2:
        print('p', wd, pearson[0])
    if spearman.correlation > 0.6 or spearman.correlation < -0.6:
        print('s', wd, spearman.correlation)
