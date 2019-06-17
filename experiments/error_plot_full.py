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
    results a tuple (union_cardinality, error)
    '''
    with open(fn, 'r') as f:
        x, y, z, je = np.loadtxt(f, usecols=(0, 1, 2, 4), unpack=True)
    u = x + y - z  # union cardinality
    j = z / u  # true jaccard
    err = abs(je - j) / j
    ulabel_int = log(u) / log(2)
    ulabel_int = ulabel_int.astype(int)
    ulabel_str = [r"$\mathregular{2}^{\mathregular{" + str(x) + "}}$" for x in ulabel_int]
    d = {'union': pd.Series(u),
         'err': pd.Series(err),
         'Method': pd.Series(label, index=range(len(u))),
         'ulabel': pd.Series(ulabel_str, index=range(len(u))),
         'jaccard': pd.Series(j),
         'constant': pd.Series(1, index=range(len(u)))}
    return pd.DataFrame(d)


if __name__ == "__main__":
    file1 = load_result('full_results-6-4-4-false.txt', "HyperMinHash: 64 buckets of 4+4 bits")
    file2 = load_result('full_results-6-0-8-false.txt', "MinHash: 64 buckets of 8 bits")
    file3 = load_result('full_results-5-0-16-false.txt', "MinHash: 32 buckets of 16 bits")

    fig = plt.figure()
    for jaccard, subplot in [(0.1, 221), (1 / 3, 222), (0.5, 223), (0.9, 224)]:
        err1 = file1.loc[file1['jaccard'] == jaccard]
        err2 = file2.loc[file2['jaccard'] == jaccard]
        err3 = file3.loc[file3['jaccard'] == jaccard]

        data = pd.concat([err1, err2, err3])
        data_agg = data.groupby(['union', 'Method']).mean()

        plt.subplot(subplot)
        ax = sns.lineplot(x='union', y='err', hue='Method', data=data)
        ax.legend_.remove()
        ax.set_yscale('log', basey=2)
        ax.set_xscale('log', basex=2)
        ax.text(0.5, 0.95, 'Jaccard index = ' + str(int(1000*jaccard)/1000), transform=ax.transAxes, horizontalalignment='center', verticalalignment='top')
        ax.set_xlabel('')
        ax.set_ylabel('')
        ymax = 2**(int(log(max(data_agg['err']))/log(2))+1)
        ymin = 2**(int(log(min(data_agg.loc[data_agg['err']>0]['err']))/log(2))-0.5)
        ax.set_ylim(ymin, ymax)
        ax.set_xlim(2, 2**28)
        #plt.tight_layout()
    if True:
        cax = fig.add_subplot(111, frameon=False)
        cax.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
        cax.grid(False)
        cax.legend(ax.get_lines(), ["HyperMinHash: 64 buckets of 4+4 bits", "MinHash: 64 buckets of 8 bits", "MinHash: 32 buckets of 16 bits"], loc='upper center', bbox_to_anchor=(0.5, -0.1))
        cax.set_xlabel("Union cardinality")
        cax.set_ylabel("Jaccard Index\nMean relative error (log plot)")

    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(6, 6)
    fig.savefig('full_comparisons' + '.png', dpi=300, bbox_inches='tight')
