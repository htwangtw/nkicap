import json
from pathlib import Path

import numpy as np
import pandas as pd

from .utils import get_project_path, read_tsv


def _fetch_margulies_gradient():
    """Load Margulies gradients in Schaefer 100 space"""
    path_dm_gradient = (
        Path(get_project_path()) / "data/hcp/hcp_embed_1-10_Schaefer1000_7Networks.txt"
    )
    return read_tsv(path_dm_gradient, header=None, names=list(range(1, 11)))


def map_space(cap_val):
    """Calculate the correlation of CAP map and top 3 Margulies gradients."""
    dm_gradient = _fetch_margulies_gradient()

    gs = []
    for i in range(3):
        dm = dm_gradient[i + 1]
        gs.append(np.corrcoef(cap_val[:1000], dm)[0, 1])
    return tuple(gs)


def cap_to_gradient(data_path=None):
    """Map all cap map to gradient space on real data."""
    if Path(data_path).exists:
        return read_tsv(data_path)
    # load data collection
    path_cap_collection = Path(get_project_path()) / "data/cap.json"
    with open(path_cap_collection) as json_file:
        path_cap = json.load(json_file)

    # load group cap and map to gradient space
    path_group_cap = path_cap["group"]
    group_cap = read_tsv(path_group_cap, index_col=0)
    gradient_space = {
        label: {"group": map_space(cap_val)} for label, cap_val in group_cap.items()
    }

    # load subject cap and map to gradient space
    for sub, path in path_cap["subject"].items():
        sub_cap = read_tsv(path, index_col=0)
        for label, cap_val in sub_cap.items():
            gradient_space[label][sub] = map_space(cap_val)

    # covert to dataframe
    collect = []
    for key in gradient_space:
        df = pd.DataFrame(
            gradient_space[key], index=[f"Gradient {i+1}" for i in range(3)]
        ).T
        df["CAP"] = key[-2:]
        df.index.name = "participant_id"
        df = df.reset_index()
        collect.append(df)
    gradient_space = pd.concat(collect, axis=0)
    if data_path:
        gradient_space.to_csv(data_path, sep="\t", index=False)
    return gradient_space
