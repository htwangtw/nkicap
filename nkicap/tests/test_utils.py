from pathlib import Path

import pytest

from ..utils import Data, get_project_path, read_tsv
from .utils import get_test_data_path

testdata = Path(get_test_data_path()) / "file.tsv"
testmriq = Path(get_test_data_path()) / "mriq.tsv"

testcsv = Path(get_test_data_path()) / "file_csv.csv"


def test_load_data():
    d = Data(datapath=testdata, mriq_label=testmriq)
    m = d.load("mriq_")
    assert m.shape[1] == 3
    m = d.load()
    assert m.shape[1] == 13
    pytest.raises(KeyError, d.load, keyword="blah")


def test_drop_mriq():
    d = Data(datapath=testdata, mriq_label=testmriq, mriq_drop=["mriq_01"])
    m = d.load("mriq_")
    assert m.shape[1] == 2


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
    pytest.raises(Exception, read_tsv, testcsv, sep=",")
