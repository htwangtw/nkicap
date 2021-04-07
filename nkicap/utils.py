from pathlib import Path
import warnings
import pandas as pd


def load_data(keyword=None, datapath="data/enhanced_nki.tsv"):
    """BIDS tsv file loader with keywords
    The first column must be subject ID
    """
    dataset = pd.read_csv(datapath, sep="\t", index_col=0)
    if keyword is None:
        return dataset

    col = [i for i in dataset.columns.tolist() if keyword in i]
    if col:
        return dataset[col]
    else:
        raise KeyError(f"No column with keyword {keyword} was found")


def get_project_path():
    return Path(__file__).absolute().parents[1]


def read_tsv(filename, **kargs):
    df = pd.read_csv(filename, sep="\t", **kargs)
    if df.empty is True:
        raise ValueError(f"{filename} is empty or not a tab separated file")
    elif "," in df.columns[0]:
        warnings.warn(f"{filename} might not be a tab separated file, please check input")
        return df
    else:
        return df