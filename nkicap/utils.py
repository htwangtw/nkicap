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
