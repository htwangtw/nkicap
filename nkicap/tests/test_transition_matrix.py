from ..transition_matrix import load_transition_mat, restore_transition_mat
import numpy as np
import pandas as pd


def test_load_transition_mat():
    """Load the correct size and subject."""
    trans_mat = load_transition_mat()
    n_cap = 8
    n_subjects = 721
    assert trans_mat.shape == (n_subjects, n_cap * (n_cap - 1))


def test_restore_transition_mat():
    n_cap = 4
    tm = np.random.rand(n_cap, n_cap)
    np.fill_diagonal(tm, 0)
    labels_flatten = [f"from_cap{i+1:02d}_to_cap{j+1:02d}"
                    for i in range(n_cap)
                    for j in range(n_cap)]
    drop_col = [f"from_cap{i+1:02d}_to_cap{j+1:02d}"
            for i in range(n_cap)
            for j in range(n_cap)
            if i == j]
    cur_flatten_data = pd.DataFrame(tm.flatten(), columns=["test"], index=labels_flatten)
    cur_flatten_data = cur_flatten_data.drop(index=drop_col)

    rtm = restore_transition_mat(cur_flatten_data["test"], n_cap=n_cap)
    np.testing.assert_almost_equal(rtm.values, tm)
