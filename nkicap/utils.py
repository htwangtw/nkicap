from pathlib import Path
import warnings
import pandas as pd
import numpy as np


class Data:
    """
    Data used in this project
    The files must be tab separated files and the first column must be index.

    Parameters
    ----------
    datapath: str or Path, optional
        Path to tsv file containing the summary data, one row per subject.

    mriq_label: str or Path, optional
        Path to tsv file containing the mriq labels.
        The headers must include: "label", "full", "summary"

    mriq_drop: None or list of strings, optional
        Whether to drop certain mriq.
        None: keep all entries
        List of index: the questions to drop

    mriq_labeltype: str, optional
        Return full length questions or the shorten version in
        Wang et al.(2018)
        "label": label in format "mriq_01"
        "full": full length question
        "summary": the shorten version in Wang et al.(2018)

    References
    ----------
    Wang, et al., (2018) "Patterns of thought: Population variation in the
    associations between large-scale network organisation and self-reported
    experiences at rest" NeuroImage, 176: 518-527
    https://doi.org/10.1016/j.neuroimage.2018.04.064

    """

    def __init__(
        self,
        datapath="data/enhanced_nki.tsv",
        mriq_label="data/mriq_labels.tsv",
        mriq_drop=None,
        mriq_labeltype="full",
    ):
        """Default parameters."""
        self.dataset = read_tsv(datapath, index_col=0)
        self.variables = self.dataset.columns.tolist()
        self.mriq_label = read_tsv(mriq_label, index_col=0).T.to_dict()
        self.mriq_drop = mriq_drop
        self.mriq_labeltype = mriq_labeltype

    def load(self, keyword=None):
        """
        Load data from the full dataset.

        Parameters
        ----------
        keyword : str or None, optional.
            Keyword in the variable name. Pass None to retrieve the full dataset

        Returns
        -------
        data :  pandas.DataFrame
            Retrieved data
        """
        col = self._fetch_keyword(keyword)
        if keyword is None or "mriq" not in keyword:
            return self.dataset[col]

        labels = self.mriq_label.copy()
        if self.mriq_drop is not None:
            for l in self.mriq_drop:
                labels.pop(l)
                col.remove(l)

        if self.mriq_labeltype != "label":
            labels = {k: v[self.mriq_labeltype] for k, v in labels.items()}
            data = self.dataset[col]
            data = data.rename(columns=labels)
        return data

    def _fetch_keyword(self, keyword):
        """Get columns with a keyword"""
        if keyword is None:
            col = self.variables
        else:
            col = [i for i in self.variables if keyword in i]

        if not col:
            raise KeyError(f"No column with keyword {keyword} was found")
        return col


def get_project_path():
    """get absolute system path of this project"""
    return Path(__file__).absolute().parents[1]


def _check_tsv(df):
    """check if file is tsv"""
    if df.empty is True:
        raise ValueError("File is empty or not a tab separated file.")
    elif "," in df.columns[0]:
        warnings.warn(
            "File is might not be a tab separated file, please check input"
        )
        return df
    else:
        return df


def read_tsv(filename, **kargs):
    """
    Read tsv file

    Parameters
    ----------
    filename: str or Path
        Path to tsv file

    **kargs:
        other inputs pass to panda.read_csv
    """
    if kargs.get("sep", False):
        raise Exception("There's not need to provide input for `sep`.")

    df = pd.read_csv(filename, sep="\t", **kargs)
    return _check_tsv(df)
