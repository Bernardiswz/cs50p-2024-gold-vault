"""
Contains the error messages to be used as attributes of the parser package's exceptions classes. Also used
for printing and displaying output for user.
"""

__all__ = ["PATHS_LIST_LEN_ERROR", "PATH_NOT_FOUND_ERROR", "INVALID_PATH_TYPE_ERROR", "USAGE"]


PATHS_LIST_LEN_ERROR: str = "Error: Lengths of input and output paths list must match."
PATH_NOT_FOUND_ERROR: str = "Error: Path '{}' does not exist."
INVALID_PATH_TYPE_ERROR: str = "Error: Path '{}' is of an invalid type. Must be file, directory or link."
USAGE: str = "usage: gvault (-e | --encrypt | -d | --decrypt) input -o OUTPUT"
