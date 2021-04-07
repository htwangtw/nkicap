"""
Get CAP data and MRIQ of the current sample.
Only need to be ran once for tidying things up, but keep it here for book keeping.
"""
from pathlib import Path
import pandas as pd
import numpy as np

from nkicap import get_project_path, read_tsv


PARTICIPANTS = "enhanced_nki/participants.tsv"
MRIQ = "enhanced_nki/mriq.tsv"
CAP_OCC = "enhanced_nki/desc-cap_occurence.tsv"
CAP_DUR = "enhanced_nki/desc-cap_duration.tsv"
CAP_GROUP = "enhanced_nki/desc-cap_groupmap.tsv"
CAP_ROI = "enhanced_nki/desg.tsv"


def fetch_dataset():
    """
    Get CAP data and MRIQ of the current sample

    Return
    ------
    dataset: dict
        A ditionaary that contains path to CAP maps
    master: pd.DataFrame
        all individual differences data in one place, including CAP derivatives, mriq and basic demographics.

    """
    data_dir = get_project_path() / "data"
    participants = read_tsv(data_dir / PARTICIPANTS, index_col=0).replace(
        {"sex": {0: "F", 1: "M"}}
    )
    mriq = (
        read_tsv(data_dir / MRIQ, index_col=0).replace({"MD": np.nan}).dropna()
    )
    occ = read_tsv(data_dir / CAP_OCC, index_col=0)
    dur = read_tsv(data_dir / CAP_DUR, index_col=0)
    roi = read_tsv(data_dir / CAP_ROI, index_col=0)
    master = pd.concat([participants, mriq, occ, dur], axis=1, join="inner")

    dataset = {
        "group": f"data/{CAP_GROUP}",
        "subject": {},
        "roi": roi.values.squeeze().tolist(),
    }
    for subject in master.index.tolist():
        sub_cap = f"data/enhanced_nki/sub-{subject}/sub-{subject}_desc-capmap_bold.tsv"
        dataset["subject"][subject] = sub_cap
    return dataset, master


if __name__ == "__main__":
    dataset, master = fetch_dataset()
    master.to_csv(get_project_path() / "data" / "enhanced_nki.tsv", sep="\t")

    import json

    with open(get_project_path() / "data" / "cap.json", "w") as fp:
        json.dump(dataset, fp, indent=2)


def test_fetch_dataset():
    """
    This test is only suitable to run locally with the full data dir
    """
    dataset, master = fetch_dataset()
    assert len(dataset["subject"]) == 711
    assert len(dataset["roi"]) == 1054
    assert dataset["group"] == "data/enhanced_nki/desc-cap_groupmap.tsv"
    assert master.shape[0] == 711
    assert type(dataset["roi"]) == list
