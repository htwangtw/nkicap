import numpy as np
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from .utils import read_tsv, get_project_path


def _fetch_margulies_gradient():
    """Load Margulies gradients in Schaefer 100 space"""
    path_dm_gradient = Path(get_project_path()) / "data/hcp/hcp_embed_1-10_Schaefer1000_7Networks.txt"
    return read_tsv(path_dm_gradient, header=None, names=list(range(1, 11)))


def map_space(cap_val):
    """Calculate the correlation of CAP map and top 3 Margulies gradients."""
    dm_gradient = _fetch_margulies_gradient()

    gs = []
    for i in range(3):
        dm = dm_gradient[i + 1]
        gs.append(np.corrcoef(cap_val[:1000], dm)[0, 1])
    return tuple(gs)
