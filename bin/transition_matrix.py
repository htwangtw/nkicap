"""Flatten transition matrix for subjects"""
import itertools
from nkicap.utils import get_project_path
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from cca_zoo.models import PMD
from seaborn.palettes import color_palette
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import ShuffleSplit

from nkicap import Data, load_transition_mat, restore_transition_mat


# not the best way to set random seed, but current only possible way
np.random.seed(123)

# load data
transitions = load_transition_mat()
data = Data(mriq_labeltype="stats")
mriq = data.load("mriq_")

# match the subjects
subjects = mriq.index
transitions = transitions.loc[subjects, :]

# zscore
standard = StandardScaler()
z_transitions = standard.fit_transform(transitions.values)
z_mriq = standard.fit_transform(mriq.values)

# train cca to get best hyper parameter
latent_dims = 1
c1 = np.arange(1, 7)
c2 = np.arange(1, 5)
param_candidates = {'c': list(itertools.product(c1, c2))}

train_model = PMD(latent_dims=latent_dims, max_iter=10000)
train_model = train_model.gridsearch_fit(z_transitions, z_mriq,
                                         param_candidates=param_candidates,
                                         verbose=False, plot=True, jobs=1)

t_brain, t_thoughts = train_model.weights_list
print(train_model.get_params())
trained_c = train_model.c


latent_dims = int(min(trained_c) ** 2)
model = PMD(c=trained_c, latent_dims=latent_dims, max_iter=10000)
model.fit(z_transitions, z_mriq)
brain, thoughts = model.weights_list
can_corr = model.train_correlations[0][1]
np.testing.assert_almost_equal(t_brain, brain[:, 0:1])
np.testing.assert_almost_equal(t_thoughts, thoughts[:, 0:1])

# make them into dataframe
brain = pd.DataFrame(brain, index=transitions.columns,
                     columns=[f"Mode {i + 1}" for i in range(latent_dims)])
thoughts_cca = pd.DataFrame(thoughts, index=mriq.columns,
                        columns=[f"Mode {i + 1}" for i in range(latent_dims)])

# plot the weights
n_cap = 8
cap_label = [f"cap{i + 1:02d}" for i in range(n_cap)]
for comp in range(latent_dims):
    restored = restore_transition_mat(brain[f"Mode {comp + 1}"].T)
    plt.figure()
    sns.heatmap(restored, center=0, cmap="RdBu_r", square=True)
    plt.title(f"Mode {comp + 1} (CC={can_corr[comp]})")
    plt.ylabel("To")
    plt.xlabel("From")
    plt.savefig(get_project_path() / f"results/transition_matrix/mode{comp + 1: 02d}_cap-transition.png")

plt.figure(figsize=(13, 7))
sns.heatmap(thoughts_cca, center=0, cmap="RdBu_r", square=True)
plt.title(f"MRIQ")
plt.savefig(get_project_path() / f"results/transition_matrix/mriq.png")

# permutation testing from
# https://github.com/andersonwinkler/PermCCA/blob/6098d35da79618588b8763c5b4a519438703dba4/permcca.m#L131-L164

n_permutation = 1000
rng = np.random.RandomState(42)
lW, cnt  = np.zeros(latent_dims), np.zeros(latent_dims)
for i in range(n_permutation):
    print(f"Permutation {1 + i} / {n_permutation} ")
    if i == 0:
        X_perm = z_transitions
        Y_perm = z_mriq
    else:
        x_idx = rng.permutation(710)
        y_idx = rng.permutation(710)
        X_perm = z_transitions[x_idx]
        Y_perm = z_mriq[y_idx]
    for k in range(latent_dims):
        if (latent_dims - k) >= min(trained_c) ** 2:  # limitation of PMD
            print(f"Mode {1 + k} of {latent_dims}")
            perm_model = PMD(c=trained_c,
                             latent_dims=(latent_dims - k),
                             max_iter=100)
            perm_model.fit(X_perm[:, k:], Y_perm[:, k:])
            r_perm = perm_model.train_correlations[0][1]
            lWtmp = -np.cumsum(np.log(1 - r_perm ** 2)[::-1])[::-1]
            lW[k] = lWtmp[0]
    if i == 0:
        lw1 = lW
    cnt = cnt + (lW >= lw1)

punc  = cnt / n_permutation
pfwer = pd.DataFrame(punc).cummax().values
print(pfwer)