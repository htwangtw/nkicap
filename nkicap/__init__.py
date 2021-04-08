"""
Data analysis suit of the CAP project
-------------------------------------

"""
from .utils import load_data

__all__ = [load_data, "plotting", "__version__"]  # not allowing scripts to be read
