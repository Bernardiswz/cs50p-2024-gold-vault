"""
This module stores the typing protocol of ParserValidator objects to optmize type hinting.

The ParserValidator protocol contains the expected structure of methods and return types
for static type checking.

Methods:
- validate: Calls _validate_io_paths.
- _validate_io_paths: Calls _validate_io_paths_list_len and _validate_input_paths.
- _validate_io_paths_list_len: Validates for matching lenght of args parsed as input and output.
- _validate_input_paths:
    Iterates over parse_args parameter and calls _validate_path_exists and _validate_path_type
    giving current input path as argument.
- _validate_path_exists: Raise PathNotFoundError if not os.path.exists.
- _validate_path_type: Raises InvalidPathTypeError if not os.path.isfile, os.path.isdir or os.path.islink.
"""

from typing import List, Protocol, runtime_checkable

__all__ = ["ParserValidator"]


@runtime_checkable
class ParserValidator(Protocol):
    def validate(self) -> None:  # pragma: no cover
        ...

    def _validate_io_paths(self) -> None:  # pragma: no cover
        ...

    def _validate_io_paths_list_len(self) -> None:  # pragma: no cover
        ...

    def _validate_input_paths(self, paths_list: List[str]) -> None:  # pragma: no cover
        ...

    def _validate_path_exists(self, path: str) -> None:  # pragma: no cover
        ...

    def _validate_path_type(self, path: str) -> None:  # pragma: no cover
        ...
