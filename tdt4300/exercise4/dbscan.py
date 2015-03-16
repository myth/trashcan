# -*- coding: utf-8 -*-

import numpy as np
from sys import argv

EPS = float(argv[2])
MINPTS = 3

POINTS = np.array([
    [2.0,4.0],
    [4.0,17.0],
    [5.0,14.0],
    [5.0,7.0],
    [5.0,4.0],
    [6.0,19.0],
    [7.0,17.0],
    [7.0,4.0],
    [8.0,18.0],
    [9.0,15.0],
    [9.0,4.0],
    [12.0,12.0],
    [12.0,9.0],
    [14.0,13.0],
    [14.0,11.0],
    [15.0,8.0],
    [16.0,13.0],
    [17.0,11.0]
])

from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.datasets.samples_generator import make_blobs

db = DBSCAN(eps=EPS, min_samples=MINPTS, metric='euclidean').fit(POINTS)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_



import matplotlib.pyplot as plt
from matplotlib.pyplot import *

uniq_labels = set(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(uniq_labels)))
for k, col in zip(uniq_labels, colors):
    if k == -1:
        col = 'k'

    class_member_mask = (labels == k)

    xy = POINTS[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=14)

    xy = POINTS[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=6)

plt.title(argv[1])

savefig("clustering-%s" % argv[1].replace('.',''), ext="png", close=True, verbose=True)
