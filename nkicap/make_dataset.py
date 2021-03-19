"""
parse dataset
"""
from pathlib import Path
import pandas as pd


PARTICIPANTS = "enhanced_nki/participants.tsv"
MRIQ = "enhanced_nki/ses-BAS1_mriq.tsv"
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
        A ditionaary that contains relevant data

    """
    data_dir = _get_project_path() / "data"
    participants = _read_tsv(data_dir / PARTICIPANTS).replace({"sex": {0: "F", 1: "M"}})
    mriq = _read_tsv(data_dir / MRIQ).dropna().dropna()
    occ = _read_tsv(data_dir / CAP_OCC)
    dur = _read_tsv(data_dir / CAP_DUR)
    roi = _read_tsv(data_dir / CAP_ROI)
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


def _get_project_path():
    return Path(__file__).absolute().parents[1]


def _read_tsv(filename):
    return pd.read_csv(filename, index_col=0, sep="\t")


if __name__ == "__main__":
    dataset, master = fetch_dataset()
    master.to_csv(_get_project_path() / "data" / "enhanced_nki.tsv", sep="\t")

    import json

    with open(_get_project_path() / "data" / "cap.json", "w") as fp:
        json.dump(dataset, fp, indent=2)


def test_fetch_dataset():
    dataset, master = fetch_dataset()
    assert len(dataset["subject"]) == 711
    assert len(dataset["roi"]) == 1054
    assert dataset["group"] == "data/enhanced_nki/desc-cap_groupmap.tsv"
    assert master.shape[0] == 711
    assert type(dataset["roi"]) == list


def test_get_project_path():
    p = _get_project_path()
    assert p.name == "nkicap"
