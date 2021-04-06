"""
project cap maps to gradient space
"""
import numpy as np


from brainspace.datasets import load_group_fc, load_parcellation
from brainspace.gradient import GradientMaps
from brainspace.utils.parcellation import map_to_labels


# First load mean HCP connectivity matrix in Schaefer
conn_matrix = load_group_fc("schaefer", scale=1000)
labeling = load_parcellation("schaefer", scale=1000, join=True)

# Ask for 3 gradients (default)
gm = GradientMaps(n_components=3, random_state=0)
gm.fit(conn_matrix)

mask = labeling != 0

hcp_de = []
for i in range(3):
    # map the gradient to the parcels
    grad = map_to_labels(gm.gradients_[:, i], labeling, mask=mask, fill=np.nan)
    hcp_de.append(hcp_de)
