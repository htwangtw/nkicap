from ..utils import load_data
from .utils import get_test_data_path

import pytest
from pathlib import Path

testdata = Path(get_test_data_path()) / "file.tsv"


def test_load_data():
    d = load_data("mriq", datapath=testdata)
    assert d.shape[1] == 3
    d = load_data(datapath=testdata)
    assert d.shape[1] == 13
    pytest.raises(KeyError, load_data, "blah", datapath=testdata)
