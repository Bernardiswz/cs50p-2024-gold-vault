import argparse
import pytest
from typing import List
from unittest.mock import patch, MagicMock
from gvault.parser.factories import ParserValidatorFactory  # type: ignore
from gvault.parser.parser_types import ParserValidator  # type: ignore
from gvault.parser.error_handling.parser_exceptions import (  # type: ignore
    PathsListLenError,
    PathNotFoundError,
    InvalidPathTypeError,
)


__all__ = ["TestParserValidator"]


class TestParserValidator:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.mock_parse_args: MagicMock = MagicMock(spec=argparse.Namespace)
        self.parser_validator: ParserValidator = ParserValidatorFactory.create_validator(self.mock_parse_args)

    def test_validate_calls(self) -> None:
        with patch.object(self.parser_validator, "_validate_io_paths") as mock_io_paths:
            self.parser_validator.validate()
            mock_io_paths.assert_called_once()

    def test_validate_io_paths_calls(self) -> None:
        self.mock_parse_args.input_paths = ["/path/to/input1", "/path/to/input2"]
        self.mock_parse_args.output_paths = ["/path/to/output1", "/path/to/output2"]

        with patch.object(
            self.parser_validator, "_validate_io_paths_list_len"
        ) as mock_validate_io_paths_list_len, patch.object(
            self.parser_validator, "_validate_paths"
        ) as mock_validate_paths:
            self.parser_validator._validate_io_paths()

            mock_validate_io_paths_list_len.assert_called_once()
            mock_validate_paths.assert_any_call(self.mock_parse_args.input_paths)
            mock_validate_paths.assert_any_call(self.mock_parse_args.output_paths)

    def test_validate_paths_calls(self):
        with patch.object(self.parser_validator, "_validate_path_exists") as mock_exists, patch.object(
            self.parser_validator, "_validate_path_type"
        ) as mock_type:
            self.parser_validator._validate_paths(["/file1.txt", "/file2.txt"])
            mock_exists.assert_any_call("/file1.txt")
            mock_exists.assert_any_call("/file2.txt")
            mock_type.assert_any_call("/file1.txt")
            mock_type.assert_any_call("/file2.txt")

    def test_validate_io_paths_list_len_invalid(self) -> None:
        self.mock_parse_args.input_paths = ["/path1"]
        self.mock_parse_args.output_paths = ["/path1", "/path2"]

        with pytest.raises(PathsListLenError):
            self.parser_validator._validate_io_paths_list_len()

    def test_validate_io_paths_list_len_valid(self) -> None:
        self.mock_parse_args.input_paths = ["/path1"]
        self.mock_parse_args.output_paths = ["/path1"]
        self.parser_validator._validate_io_paths_list_len()

    def test_validate_path_exists(self) -> None:
        with patch("os.path.exists") as mock_exists:
            # Path exists if path == "/existing/path"
            mock_exists.side_effect = lambda x: x == "/existing/path"

            self.parser_validator._validate_path_exists("/existing/path")

            # Testing for non-existing path
            with pytest.raises(PathNotFoundError):
                self.parser_validator._validate_path_exists("/non_existing/path")

    def test_validate_invalid_path_type(self):
        with patch("os.path.isfile", return_value=False) as mock_isfile, patch(
            "os.path.isdir", return_value=False
        ) as mock_isdir, patch("os.path.islink", return_value=False) as mock_islink:
            with pytest.raises(InvalidPathTypeError):
                self.parser_validator._validate_path_type(";")

            mock_isfile.assert_called_once_with(";")
            mock_isdir.assert_called_once_with(";")
            mock_islink.assert_called_once_with(";")

    def test_validate_path_type_is_file(self) -> None:
        with patch("os.path.isfile") as mock_isfile:
            mock_isfile.side_effect = lambda path: path == "/file.txt"
            self.parser_validator._validate_path_type("/file.txt")
            mock_isfile.assert_called_once_with("/file.txt")

    def test_validate_path_type_is_dir(self) -> None:
        with patch("os.path.isdir") as mock_isdir:
            mock_isdir.side_effect = lambda path: path == "/directory"
            self.parser_validator._validate_path_type("/directory")

    def test_validate_path_type_is_link(self) -> None:
        with patch("os.path.islink") as mock_islink:
            mock_islink.side_effect = lambda path: path == "/symlink"
            self.parser_validator._validate_path_type("/symlink")
            mock_islink.assert_called_once_with("/symlink")

    def test_validate_paths_valid(self) -> None:
        paths_list: List[str] = ["/path/to/input1", "/path/to/input2"]

        # Valid paths case (None return)
        with patch.object(
            self.parser_validator, "_validate_path_exists", return_value=None
        ) as mock_validate_path_exists, patch.object(
            self.parser_validator, "_validate_path_type", return_value=None
        ) as mock_validate_path_type:
            self.parser_validator._validate_paths(paths_list)

            # Assert _validate_path_exists is called with each path
            for path in paths_list:
                mock_validate_path_exists.assert_any_call(path)
                mock_validate_path_type.assert_any_call(path)

    def test_validate_paths_invalid_path_exists(self) -> None:
        paths_list = ["/invalid/path"]

        # Invalid path should raise PathNotFoundError
        with patch.object(
            self.parser_validator,
            "_validate_path_exists",
            side_effect=PathNotFoundError("/invalid/path"),
        ) as mock_validate_path_exists, patch.object(
            self.parser_validator, "_validate_path_type"
        ) as mock_validate_path_type:
            with pytest.raises(PathNotFoundError):
                self.parser_validator._validate_paths(paths_list)

            mock_validate_path_exists.assert_called_once_with("/invalid/path")
            mock_validate_path_type.assert_not_called()

    def test_validate_paths_invalid_path_type(self) -> None:
        paths_list = ["/invalid/path"]

        # Invalid path type should raise InvalidPathTypeError
        with patch.object(
            self.parser_validator, "_validate_path_exists", return_value=None
        ) as mock_validate_path_exists, patch.object(
            self.parser_validator,
            "_validate_path_type",
            side_effect=InvalidPathTypeError("/invalid/path"),
        ) as mock_validate_path_type:
            with pytest.raises(InvalidPathTypeError):
                self.parser_validator._validate_paths(paths_list)

            mock_validate_path_exists.assert_called_once_with("/invalid/path")
            mock_validate_path_type.assert_called_once_with("/invalid/path")
