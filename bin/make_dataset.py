"""
Get CAP data and MRIQ of the current sample.
Only need to be ran once for tidying things up, but keep it here for book keeping.
"""
import json
import os

import numpy as np
import pandas as pd
from scipy import io

from nkicap import get_project_path, read_tsv

SOURCE_MAT = "sourcedata/CAP_results_organized_toHaoTing.mat"
SOURCE_MRIQ = "sourcedata/ses-BAS1_mriq.csv"
PARTICIPANTS = "enhanced_nki/participants.tsv"
MRIQ = "enhanced_nki/mriq.tsv"
LABEL = "enhanced_nki/desg.tsv"
SCHAEFER = "parcellations/Schaefer2018_1000Parcels_7Networks_order.txt"
TIAN = "parcellations/Tian_Subcortex_S4_3T_label.txt"
CAP_OCC = "enhanced_nki/desc-cap_occurence.tsv"
CAP_DUR = "enhanced_nki/desc-cap_duration.tsv"
CAP_GROUP = "enhanced_nki/desc-cap_groupmap.tsv"
CAP_ROI = "enhanced_nki/desg.tsv"

data_dir = get_project_path() / "data"


def roi_labels():
    """Make ROI label refereces."""
    shaefer = pd.read_table(data_dir / SCHAEFER, header=None, index_col=0)
    tian = pd.read_table(data_dir / TIAN, header=None)
    shaefer = shaefer.rename(columns={1: "name"})
    tian = tian.rename(columns={0: "name"})
    shaefer["index"] = range(1, 1001)
    tian["index"] = range(1001, 1055)
    lablel = pd.concat(
        [shaefer.loc[:, ["index", "name"]], tian.loc[:, ["index", "name"]]],
        ignore_index=True,
    )
    lablel.to_csv(data_dir / LABEL, index=False, sep="\t")


def source2raw():
    """Parse .mat file to txt."""
    cap_results = io.loadmat(
        data_dir / SOURCE_MAT, squeeze_me=True, simplify_cells=True
    )["CAP_results"]
    mriq_source = pd.read_csv(data_dir / SOURCE_MRIQ, index_col=0).dropna()
    mriq_source["mriq"] = np.ones(mriq_source.shape[0])

    # cap summary stats
    occ = pd.DataFrame(
        cap_results["occurence_rate"],
        index=[f"occ_cap_{i+1:02d}" for i in range(8)],
        columns=cap_results["subjects"],
    ).T
    occ.index.name = "participant_id"
    occ.to_csv(data_dir / CAP_OCC, sep="\t")

    dur = pd.DataFrame(
        cap_results["duration"],
        index=[f"dur_cap_{i+1:02d}" for i in range(8)],
        columns=cap_results["subjects"],
    ).T
    dur.index.name = "participant_id"
    dur.to_csv(data_dir / CAP_DUR, sep="\t")

    # cap map and transition matrix
    cap_labels = [f"cap_{i+1:02d}" for i in range(8)]
    for t, m, sub in zip(
        cap_results["transition"],
        cap_results["map_sub"],
        cap_results["subjects"],
    ):
        # create subject dir
        sub_path = f"enhanced_nki/sub-{sub}/"
        if not (data_dir / sub_path).exists():
            os.makedirs(str(data_dir / sub_path))
        t = pd.DataFrame(t, index=cap_labels, columns=cap_labels)
        m = pd.DataFrame(m, columns=cap_labels, index=range(1, 1055))
        t.to_csv(
            data_dir / f"enhanced_nki/sub-{sub}/sub-{sub}_desc-capmap_bold.tsv",
            sep="\t",
        )
        m.to_csv(
            data_dir / f"enhanced_nki/sub-{sub}/sub-{sub}_desc-transition.tsv",
            sep="\t",
        )

    cap_group = pd.DataFrame(
        cap_results["map_group"], columns=cap_labels, index=range(1, 1055)
    )
    cap_group.to_csv(data_dir / CAP_GROUP, sep="\t")

    # create participants info file
    participants = pd.DataFrame(
        [cap_results["age"], cap_results["sex"]],
        columns=cap_results["subjects"],
        index=["age", "sex"],
    ).T
    participants.index.name = "participant_id"
    participants = pd.concat([participants, mriq_source["mriq"]], axis=1).dropna(
        thresh=2
    )
    participants["mriq"] = participants["mriq"].fillna(0)
    participants.to_csv(data_dir / PARTICIPANTS, sep="\t")

    # save mriq
    mriq = mriq_source.loc[participants[participants["mriq"] == 1].index, :]
    mriq = mriq.drop(columns=["mriq"])
    mriq = mriq.rename(columns={"rmiq_26": "mriq_26"})
    mriq = mriq.loc[:, [f"mriq_{i+1:02d}" for i in range(31)]]
    mriq.to_csv(data_dir / MRIQ, sep="\t")


def fetch_dataset():
    """
    Get CAP data and MRIQ of the current sample.

    Return
    ------
    dataset: dict
        A ditionary that contains path to CAP maps
    master: pd.DataFrame
        all individual differences data in one place,
        including CAP derivatives, mriq and basic demographics.
    """
    participants = read_tsv(data_dir / PARTICIPANTS, index_col=0).replace(
        {"sex": {0: "F", 1: "M"}}
    )
    mriq = read_tsv(data_dir / MRIQ, index_col=0).replace({"MD": np.nan}).dropna()
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
    source2raw()
    roi_labels()
    dataset, master = fetch_dataset()
    master.to_csv(get_project_path() / "data" / "enhanced_nki.tsv", sep="\t")

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
