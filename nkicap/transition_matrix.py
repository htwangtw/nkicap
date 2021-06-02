import re

import pandas as pd
import numpy as np

from .utils import get_project_path, read_tsv


def load_transition_mat():
    """Load and flatten transition matrix."""
    transition_mat_pattern = "data/enhanced_nki/sub-*/sub-*_desc-transition.tsv"
    project_path = get_project_path()

    labels_flatten = [f"from_cap{i+1:02d}_to_cap{j+1:02d}"
                    for i in range(8)
                    for j in range(8)]

    transition_data = pd.DataFrame()
    for path_mat in project_path.glob(transition_mat_pattern):
        # get id
        subject = path_mat.name.split("_des")[0].split("sub-")[1]
        # read the matrix
        mat = read_tsv(path_mat, index_col=0).values.flatten()
        cur_flatten_data = pd.DataFrame(mat, columns=[subject], index=labels_flatten).T
        transition_data = pd.concat([transition_data, cur_flatten_data], axis=0)

    # drop self to self cells
    drop_col = [f"from_cap{i+1:02d}_to_cap{j+1:02d}"
                for i in range(8)
                for j in range(8)
                if i == j]

    transition_data = transition_data.drop(columns=drop_col).sort_index()
    return transition_data


def restore_transition_mat(transition_data, n_cap=8):
    """Restore transition matrix from the flatten state."""
    cap_label = [f"cap{i + 1:02d}" for i in range(n_cap)]
    col_names = transition_data.index
    restored = np.zeros((n_cap, n_cap))
    for name in col_names:
        i, j = [int(item) - 1 for item in re.findall("cap0([\d])", name)]
        restored[i, j] = transition_data[name]
    restored = pd.DataFrame(np.array(restored),
                    columns=cap_label,
                    index=cap_label)
    return restored
