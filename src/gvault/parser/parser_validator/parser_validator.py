"""
Module that contains the validation logic for parsed args.

Contains the ParserValidator class that will perform according validation of parse_args
before the process of encryption and decryption.
"""

import argparse
import os
from typing import List
from gvault.error_handling.exceptions.parser_exceptions import (
    InvalidPathTypeError,
    PathsListLenError,
    PathNotFoundError,
)


__all__ = ["ParserValidator"]


class ParserValidator:
    """
    Performs validation on given parse_args instance of argparse.Namespace.

    Provides the interface method 'validate'.
    """

    def __init__(self, parse_args: argparse.Namespace):
        """
        Initializes an object of ParserValidator.

        Args:
            parse_args (argparse.Namespace):
                Object that contains the usage of the program (encryption|decryption) and paths of input files and their
                respective output.
        """
        self.parse_args: argparse.Namespace = parse_args

    def validate(self) -> None:
        """
        Calls _validate_io_paths.
        """
        self._validate_io_paths()

    def _validate_io_paths(self) -> None:
        """
        Calls _validate_io_paths_list_len and _validate_input_paths giving parse_args.input_paths attr as arg.
        """
        self._validate_io_paths_list_len()
        self._validate_input_paths(self.parse_args.input_paths)

    def _validate_io_paths_list_len(self) -> None:
        """
        Check for equality in length of List[str] parse_args.input_paths and parse_args.output_paths.

        Raises:
            PathsListLenError if unmatching lengths.
        """
        if len(self.parse_args.input_paths) != len(self.parse_args.output_paths):
            raise PathsListLenError()

    def _validate_input_paths(self, paths_list: List[str]) -> None:
        """
        Iterates over each path in param List[str] paths_list and calls _validate_path_exists and _validate_path_type.

        Args:
            paths_list: (List[str]): Attr of parse_args, input and output_paths.
        """
        for path in paths_list:
            self._validate_path_exists(path)
            self._validate_path_type(path)

    def _validate_path_exists(self, path: str) -> None:
        """
        Raises PathNotFoundError if not os.path.exists param path.

        Args:
            path (str): String containing the path of the input file path to validation.

        Raises:
            PathNotFoundError if not os.path.exists(path).
        """
        if not os.path.exists(path):
            raise PathNotFoundError(path)

    def _validate_path_type(self, path: str) -> None:
        """
        Raises InvalidPathTypeError if path isn't file, dir or link.

        Args:
            path (str): String containing the path of the input file path to validation.

        Raises:
            InvalidPathTypeError if not isfile, isdir or islink (path).
        """
        if not os.path.isfile(path) and not os.path.isdir(path) and not os.path.islink(path):
            raise InvalidPathTypeError(path)
