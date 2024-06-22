import os
from typing import List
from ..error_handling.parser_exceptions import (
    InvalidPathTypeError,
    PathsListLenError,
    PathNotFoundError
)


__all__ = ["ParserValidator"]


class ParserValidator:
    def __init__(self, input_paths: List[str], output_paths: List[str]):
        self.input_paths: List[str] = input_paths
        self.output_paths: List[str] = output_paths
    
    def validate(self) -> None:
        self._validate_io_paths()

    def _validate_io_paths(self) -> None:
        self._validate_io_paths_list_len()
        self._validate_paths(self.input_paths)
        self._validate_paths(self.output_paths)

    def _validate_io_paths_list_len(self) -> None:
        if len(self.input_paths) != len(self.output_paths):
            raise PathsListLenError()
        
    def _validate_paths(self, paths_list: List[str]) -> None:
        for path in paths_list:
            self._validate_path_exists(path)
            self._validate_path_type(path)
    
    def _validate_path_exists(self, path: str) -> None:
        if not os.path.exists(path):
            raise PathNotFoundError(path)

    def _validate_path_type(self, path: str) -> None:
        if not os.path.isfile(path) or os.path.isdir(path) or os.path.islink(path):
            raise InvalidPathTypeError(path)
