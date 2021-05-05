"""
Data analysis suit of the CAP project
-------------------------------------

"""
from .utils import Data, get_project_path, read_tsv

__all__ = [
    Data,
    read_tsv,
    get_project_path,
    "plotting",
    "__version__",
]  # not allowing scripts to be read
