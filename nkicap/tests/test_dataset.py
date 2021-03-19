from ..dataset import fetch_dataset


def test_fetch_dataset():
    dataset = fetch_dataset()

    assert len(dataset["participant_id"]) == 711
    assert len(dataset["subject_cap_map"]) == 711
    assert len(dataset["roi_cap_map"]) == 1054
    assert dataset["group_cap_map"].shape == (1054, 8)
    assert dataset["cap_occurence"].shape == (711, 8)
    assert dataset["cap_duration"].shape == (711, 8)
    assert dataset["subject_cap_map"]["A00027544"].shape == (1054, 8)
