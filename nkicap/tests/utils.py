from os.path import join
from pathlib import Path


def get_test_data_path():
    return join(Path(__file__).absolute().parent, "data")
