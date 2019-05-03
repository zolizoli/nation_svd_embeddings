from os import listdir
from os.path import isdir, join

from src.svd_algebra import *

periods = [(1789, 1849), (1850, 1865), (1866, 1918), (1919, 1945),
           (1946, 1964), (1965, 1980), (1980, 1991), (1992, 2008),
           (2009, 2017)]

in_path = 'models'

models = [d for d in listdir(in_path) if isdir(join(in_path, d))]
models.sort()


def similar_for_periods(wd, n):
    for model in models:
        a = SVDAlgebra(join(in_path, model))
        sims = a.most_similar_n(wd, n)
        sims = ' '.join(sims)
        i = int(model)
        p = periods[i]
        period = str(p[0]) + '-' + str(p[1])
        print('The most similar words to %s in %s are %s' % (wd, period, sims))


def distance_for_periods(wd1, wd2):
    for model in models:
        a = SVDAlgebra(join(in_path, model))
        try:
            dist = str(a.distance(wd1, wd2))
        except Exception as e:
            dist = "word is missing"
        i = int(model)
        p = periods[i]
        period = str(p[0]) + '-' + str(p[1])
        print('The distance btw %s and %s in period %s is %s' % (wd1, wd2, period, dist))


similar_for_periods('nation', 10)

distance_for_periods('nation', 'americans')
