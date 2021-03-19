"""
parse dataset
"""
from pathlib import Path
import pandas as pd
from sklearn.utils import Bunch


PARTICIPANTS = "enhanced_nki/participants.tsv"
MRIQ = "enhanced_nki/ses-BAS1_mriq.tsv"
CAP_OCC = "enhanced_nki/desc-cap_occurence.tsv"
CAP_DUR = "enhanced_nki/desc-cap_duration.tsv"
CAP_GROUP = "enhanced_nki/desc-cap_groupmap.tsv"
CAP_ROI = "enhanced_nki/desg.tsv"
README = "enhanced_nki/README.md"


def fetch_dataset():
    """
    Get CAP data and MRIQ of the current sample

    Return
    ------
    dataset: dict
        A ditionaary that contains relevant data

    """
    data_dir = _get_data_path()
    participants = _read_tsv(data_dir / PARTICIPANTS)
    mriq = _read_tsv(data_dir / MRIQ).dropna().dropna()
    occ = _read_tsv(data_dir / CAP_OCC)
    dur = _read_tsv(data_dir / CAP_DUR)
    roi = _read_tsv(data_dir / CAP_ROI)
    master = pd.concat([participants, mriq, occ, dur], axis=1, join="inner")

    with open(data_dir / README, "r") as f:
        DESCR = f.read()

    groupmap = _read_tsv(data_dir / CAP_GROUP)
    dataset = {
        "DESCR": DESCR,
        "group_cap_map": groupmap.to_dict("list"),
        "subject_cap_map": {},
        "roi_cap_map": roi.values,
        "participant_id": master.index.tolist(),
        "age": master["age"].values,
        "sex": master["sex"].values,
        "cap_occurence": master.loc[:, "occ_cap_01":"occ_cap_08"].values,
        "cap_duration": master.loc[:, "dur_cap_01":"dur_cap_08"].values,
    }
    for subject in master.index.tolist():
        sub_cap = f"enhanced_nki/sub-{subject}/sub-{subject}_desc-capmap_bold.tsv"
        sub_cap = _read_tsv(data_dir / sub_cap).to_dict("list")
        dataset["subject_cap_map"][subject] = sub_cap
    return dataset


def _get_data_path():
    return Path(__file__).absolute().parents[1] / "data"


def _read_tsv(filename):
    return pd.read_csv(filename, index_col=0, sep="\t")
