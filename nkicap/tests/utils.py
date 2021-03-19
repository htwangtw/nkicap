from pathlib import Path
from os.path import join


def get_test_data_path():
    return join(Path(__file__).absolute().parent, "data")
