from os import listdir
from os.path import isdir, join

import numpy as np
from scipy.spatial import procrustes
from scipy.spatial.distance import cosine
from sklearn.neighbors import NearestNeighbors

from src.svd_algebra import *

periods = [(1789, 1849), (1850, 1865), (1866, 1918), (1919, 1945),
           (1946, 1964), (1965, 1980), (1980, 1991), (1992, 2008),
           (2009, 2017)]

in_path = 'models'

models = [d for d in listdir(in_path) if isdir(join(in_path, d))]
models.sort()

# get common vocabulary

vocabs = []
for model in models:
    a = SVDAlgebra(join(in_path, model))
    vocabs.append(set(a.vocabulary))
common_vocab = set.intersection(*vocabs)

aligned_models = []
a = SVDAlgebra(join(in_path, models[0]))
b = SVDAlgebra(join(in_path, models[1]))
delete_a_indices = [a.vocabulary.index(e) for e in a.vocabulary
                    if e not in common_vocab]
delete_b_indices = [b.vocabulary.index(e) for e in b.vocabulary
                    if e not in common_vocab]
new_model_a = np.delete(a.U, delete_a_indices, axis=0)
new_model_b = np.delete(b.U, delete_b_indices, axis=0)
mtx1, mtx2, disparity = procrustes(new_model_a,new_model_b)
t = (mtx1, mtx2)
aligned_models.append(t)


for i in range(2, len(models)):
    model_b = aligned_models[-1][1]
    model = SVDAlgebra(join(in_path, models[i]))
    delete_indices = [model.vocabulary.index(e) for e in model.vocabulary
                      if e not in common_vocab]
    new_model = np.delete(model.U, delete_indices, axis=0)
    mtx1, mtx2, disparity = procrustes(model_b, new_model)
    t = (mtx1, mtx2)
    aligned_models.append(t)

sorted_vocab = sorted(common_vocab)
wd_shifts = {}
for wd in common_vocab:
    if wd not in wd_shifts:
        wd_shifts[wd] = []
    i = sorted_vocab.index(wd)
    initial = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(aligned_models[0][0])
    initial_neighbors = initial.kneighbors(aligned_models[0][0][i].reshape(1, -1))
    final = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(aligned_models[-1][1])
    final_neighbors = final.kneighbors(aligned_models[-1][1][i].reshape(1, -1))
    initial_neighbors = initial_neighbors[1].tolist()[0][1:]
    final_neighbors = final_neighbors[1].tolist()[0][1:]
    initial_words = [sorted_vocab[i] for i in initial_neighbors]
    final_words = [sorted_vocab[i] for i in final_neighbors]
    for aligned_model in aligned_models:
        am = aligned_model[1]
        if sorted_vocab[wd] not in wd_shifts.keys():
            wd_shifts[sorted_vocab[wd]] = []
        for wd in initial_neighbors:
            sim = cosine(am[i], am[wd])
            wd_shifts[sorted_vocab[wd]].append(sim)
        for wd in final_neighbors:
            sim = cosine(am[i], am[wd])
            wd_shifts[sorted_vocab[wd]].append(sim)

