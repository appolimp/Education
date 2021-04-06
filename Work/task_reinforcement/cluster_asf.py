import re
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler


file_asf = r"st3_r02.asf"

# введите фоновую арматуру для вычитания из вычисленной
top_reinforcement = 10.0
bottom_reinforcement = 10.0


X = []


with open(file_asf, "r") as f:
    for line in f:
        if 'QB' in line:
            # print(line.index(line))
            # first_row = f.__next__()
            number = re.findall(r"[-+]?\d*\.\d+|\d+", line)
            X_coordinates = float(number[0]) * 1000.0
            Y_coordinates = float(number[1]) * 1000.0
            reinf_additional = round(float(number[3])-top_reinforcement, 2)
            if reinf_additional > 0:
                X.append(
                    [X_coordinates, Y_coordinates])
n_arr = np.array(X)
# print((n_arr))

db = DBSCAN(eps=800, min_samples=4).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = list(labels).count(-1)

# #############################################################################
# Plot result

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
# print(labels)
# print(n_noise)
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)
    # print(class_member_mask)
    # print(core_samples_mask)
    # print(class_member_mask)
    # print(xy)

    xy = n_arr[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=7)
    xy = n_arr[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=3)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
