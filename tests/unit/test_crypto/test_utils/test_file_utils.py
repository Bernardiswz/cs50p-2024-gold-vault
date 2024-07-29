import pytest
from unittest.mock import MagicMock, patch, mock_open
from typing import Any, Dict, Generator
from gvault.crypto.utils.file_utils import read_file, write_file, confirm_overwrite_path # type: ignore


class TestFileUtils:
    def test_read_file(self, mocker) -> None:
        mock_file: MagicMock = mock_open(read_data=b"test data")
        mocker.patch("builtins.open", mock_file)
        filepath: str = "file/path"
        result: bytes = read_file(filepath)
        mock_file.assert_called_once_with(filepath, "rb")
        assert result == b"test data"
