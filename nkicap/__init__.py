"""
Data analysis suit of the CAP project
-------------------------------------

"""
from .utils import load_data, read_tsv, get_project_path

__all__ = [
    load_data,
    read_tsv,
    get_project_path,
    "__version__",
]  # not allowing scripts to be read
