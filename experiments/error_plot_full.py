#!/usr/bin/env python

from __future__ import division, print_function

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from numpy import log
import pandas as pd
import seaborn as sns
from itertools import groupby


def load_result(fn, label):
    '''fn is a file name, label is an arbitrary string,
    results a tuple (union_cardinality, error)'''
    with open(fn, 'r') as f:
        x, y, z, je = np.loadtxt(f, usecols=(0,1,2,4), unpack=True)
    u = x + y - z # union cardinality
    j = z/u # true jaccard
    err = abs(je-j)/j
    ulabel_int = log(u/3)/log(2)
    ulabel_int = ulabel_int.astype(int)
    ulabel_str = [ r"$\mathregular{2}^{\mathregular{" + str(x) + "}}$" for x in ulabel_int]
    d = {'union': pd.Series(u),
         'err': pd.Series(err),
         'Method': pd.Series(label, index=range(len(u))),
         'ulabel': pd.Series(ulabel_str, index=range(len(u)))
          }
    return pd.DataFrame(d)



err1 = load_result('full_results-8-4-4-false.txt', "HyperMinHash: 256 buckets of 4+4 bits")
err2 = load_result('full_results-8-0-8-false.txt', "MinHash: 256 buckets of 8 bits" )
err3 = load_result('full_results-7-0-16-false.txt', "MinHash: 128 buckets of 16 bits")

data = pd.concat([err1, err2, err3])

ax = sns.pointplot(x='ulabel', y='err', hue='Method', data=data, estimator=np.mean, palette='Set2', dodge=True, markers=['o', 'D', '>'], scale=1.5)
ax.set_ylim(0,2)
ax.set_xlabel("Intersection Cardinality (log plot) \n Union Cardinality (x3)")
ax.set_ylabel("Jaccard Index \n Mean relative error (log plot)")
ax.set_yscale('log', basey=2)
ax.set_ylim(1./32, 2)
plt.tight_layout()
fig = matplotlib.pyplot.gcf()
fig.set_size_inches(11, 6)
fig.savefig('full_comparisons.png', dpi=300)
