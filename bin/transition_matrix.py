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

from nkicap import Data, load_transition_mat, restore_transition_mat


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

# train cca
latent_dims = 5
c1 = np.arange(1, 7, 0.1)
c2 = np.arange(1, 5, 0.1)
param_candidates = {'c': list(itertools.product(c1, c2))}
np.random.default_rng(42)  # fix the random seed
wrap_pmd = PMD(latent_dims=latent_dims)
wrap_pmd = wrap_pmd.gridsearch_fit(z_transitions, z_mriq,
                                   param_candidates=param_candidates,
                                   verbose=True, plot=True, jobs=15)

brain, thoughts = wrap_pmd.weights_list
# make them into dataframe


# plot the weights
n_cap = 8
cap_label = [f"cap{i + 1:02d}" for i in range(n_cap)]
thoughts_cca = pd.DataFrame()
for comp, (b, t) in enumerate(zip(brain.T, thoughts.T)):
    restored = restore_transition_mat(b)
    thoughts_labeled = pd.DataFrame(t,
                                    columns=[f"Mode {comp + 1}"],
                                    index=mriq.columns)

    thoughts_cca = pd.concat([thoughts_cca, thoughts_labeled], axis=1)

    plt.figure()
    sns.heatmap(restored, center=0, cmap="RdBu_r", square=True)
    plt.title(f"Mode {comp + 1}: CAP transition matrix")
    plt.savefig(get_project_path() / f"results/mode{comp + 1: 02d}_cap-transition.png")

plt.figure(figsize=(13, 7))
sns.heatmap(thoughts_cca, center=0, cmap="RdBu_r", square=True)
plt.title(f"MRIQ")
plt.savefig(get_project_path() / f"results/mriq.png")

