from unittest.mock import MagicMock, mock_open
from typing import Any, Dict, Generator
from gvault.crypto.utils.file_utils import read_file, write_file, confirm_overwrite_path # type: ignore


__all__ = ["TestFileUtils"]


class TestFileUtils:
    def test_read_file(self, mocker: Generator) -> None:
        mock_file: MagicMock = mock_open(read_data=b"test data")
        mocker.patch("builtins.open", mock_file)
        filepath: str = "file/path"
        result: bytes = read_file(filepath)
        mock_file.assert_called_once_with(filepath, "rb")
        assert result == b"test data"

    def test_write_file(self, mocker: Generator) -> None:
        mock_file: Any = mock_open()
        mocker.patch("builtins.open", mock_file)
        filepath: str = "file/path"
        data: bytes = b"test data"
        write_file(filepath, data)
        mock_file.assert_called_once_with(filepath, "wb")
        mock_file().write.assert_called_once_with(data)

    def test_confirm_overwrite_path_yes(self, mocker: Generator):
        mock_input: Any = mocker.patch("builtins.input", return_value="y")
        path: str = "some/path"
        result: bool = confirm_overwrite_path(path)
        mock_input.assert_called_once_with(f"Path '{path}' already exists, overwrite? [y/n]")
        assert result is True

    def test_confirm_overwrite_path_no(self, mocker: Generator):
        mock_input: Any = mocker.patch("builtins.input", return_value="n")
        path: str = "some/path"
        result: bool = confirm_overwrite_path(path)
        mock_input.assert_called_once_with(f"Path '{path}' already exists, overwrite? [y/n]")
        assert result is False
