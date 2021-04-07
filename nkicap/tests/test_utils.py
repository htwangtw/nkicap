from ..utils import load_data, get_project_path, read_tsv
from .utils import get_test_data_path

import pytest
from pathlib import Path

testdata = Path(get_test_data_path()) / "file.tsv"
testcsv = Path(get_test_data_path()) / "file_csv.csv"


def test_load_data():
    d = load_data("mriq", datapath=testdata)
    assert d.shape[1] == 3
    d = load_data(datapath=testdata)
    assert d.shape[1] == 13
    pytest.raises(KeyError, load_data, "blah", datapath=testdata)


def test_get_project_path():
    p = get_project_path()
    assert p.name == "nkicap"

def test_read_tsv():
    f = read_tsv(testdata)
    assert f.index.tolist() == list(range(4))

    f_arg = read_tsv(testdata, index_col=0)
    assert f_arg.index.tolist()[0] == "A00123"
    pytest.raises(ValueError, read_tsv, testcsv, index_col=0)
    pytest.warns(UserWarning, read_tsv, testcsv)
