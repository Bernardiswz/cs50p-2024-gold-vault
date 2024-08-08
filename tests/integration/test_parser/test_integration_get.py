import argparse
import os
import pytest
from typing import Any, Dict, Generator, List, Union
from _pytest.capture import CaptureResult
from gvault.parser import get_parser  # type: ignore
from gvault.error_handling.messages.parser_messages import (  # type: ignore
    USAGE,
    PATHS_LIST_LEN_ERROR,
    PATH_NOT_FOUND_ERROR,
)


__all__ = ["TestGet"]


class TestGet:
    TEST_GET_DIRECTORY: str = "get_dir"
    TEST_GET_INNER_DIR: str = os.path.join(TEST_GET_DIRECTORY, "inner_directory")
    FILE1_PATH: str = os.path.join(TEST_GET_DIRECTORY, "file1.txt")
    FILE2_PATH: str = os.path.join(TEST_GET_DIRECTORY, "file2.txt")
    INVALID_FILE_PATH: str = os.path.join(TEST_GET_DIRECTORY, "invalid_file")
    INNER_FILE1_PATH: str = os.path.join(TEST_GET_INNER_DIR, "inner_file1.txt")
    FILES_LIST: List[str] = [FILE1_PATH, FILE2_PATH, INNER_FILE1_PATH]

    @pytest.fixture(autouse=True)
    def setup_method(self, monkeypatch: pytest.MonkeyPatch) -> Generator[Any, Any, Any]:
        self.monkeypatch: pytest.MonkeyPatch = monkeypatch  # Usage on parsing of args
        self.make_test_get_dirs()
        self.write_test_files()
        yield
        self.teardown_method()

    def make_test_get_dirs(self) -> None:
        os.makedirs(self.TEST_GET_DIRECTORY, exist_ok=True)
        os.makedirs(self.TEST_GET_INNER_DIR, exist_ok=True)

    def write_test_files(self) -> None:
        for file_path in self.FILES_LIST:
            with open(file_path, "w") as file:
                file.write("Some content")

    def teardown_method(self) -> None:
        self.remove_test_files()
        self.remove_setup_dir(self.TEST_GET_INNER_DIR)
        self.remove_setup_dir(self.TEST_GET_DIRECTORY)

    def remove_test_files(self) -> None:
        for file_path in self.FILES_LIST:
            if os.path.exists(file_path):
                os.remove(file_path)

    def remove_setup_dir(self, dir: str) -> None:
        if os.path.exists(dir):
            os.rmdir(dir)

    def _set_monkeypatch_argv(self, argv: List[str]) -> None:
        self.monkeypatch.setattr("sys.argv", argv)

    def _assert_err_message_in_outerr(self, error_message: str, capsys: pytest.CaptureFixture) -> None:
        captured: CaptureResult = capsys.readouterr()
        assert error_message in captured.out or error_message in captured.err

    @pytest.mark.parametrize(
        "argv, expected",
        [
            (
                ["script.py", "-e", FILE1_PATH, "-o", "output_file1.txt"],
                {"input_paths": [FILE1_PATH], "output_paths": ["output_file1.txt"], "encrypt": True, "decrypt": False},
            ),
            (
                ["script.py", "-d", TEST_GET_INNER_DIR, "-o" "output_dir"],
                {
                    "input_paths": [TEST_GET_INNER_DIR],
                    "output_paths": ["output_dir"],
                    "encrypt": False,
                    "decrypt": True,
                },
            ),
            (
                ["script.py", "--encrypt", FILE1_PATH, FILE2_PATH, "--output_paths", "output1.txt", "output2.txt"],
                {
                    "input_paths": [FILE1_PATH, FILE2_PATH],
                    "output_paths": ["output1.txt", "output2.txt"],
                    "encrypt": True,
                    "decrypt": False,
                },
            ),
        ],
    )
    def test_valid_usage(self, argv: List[str], expected: Dict[str, List[str]]) -> None:
        self._set_monkeypatch_argv(argv)
        parse_args: Union[argparse.Namespace, None] = get_parser()
        assert isinstance(parse_args, argparse.Namespace)
        self._assert_expected_parse_args_io_paths(parse_args, expected)
        self._assert_expected_parse_args_flags(parse_args, expected)

    def _assert_expected_parse_args_io_paths(
            self, 
            parse_args: argparse.Namespace, 
            expected: Dict[str, List[str]]
        ) -> None:
        assert parse_args.input_paths == expected["input_paths"]
        assert parse_args.output_paths == expected["output_paths"]

    def _assert_expected_parse_args_flags(self, parse_args: argparse.Namespace, expected: Dict[str, List[str]]) -> None:
        assert parse_args.encrypt == expected["encrypt"]
        assert parse_args.decrypt == expected["decrypt"]

    @pytest.mark.parametrize("argv", [["script.py", "--find", "file1_py", "-output file2.py"]])
    def test_default_invalid_usage(self, argv: List[str], capsys: pytest.CaptureFixture) -> None:
        self._set_monkeypatch_argv(argv)
        parse_args: Union[argparse.Namespace, None] = None
        with pytest.raises(SystemExit) as excinfo:
            parse_args = get_parser()
        assert parse_args is None
        self._assert_excinfo_expected(excinfo, expected_code=2)
        self._assert_err_message_in_outerr(USAGE, capsys)

    @pytest.mark.parametrize(
        "argv",
        [
            ["script.py", "-e", FILE1_PATH, FILE2_PATH, "-o", "output_file1.txt"],
            ["script.py", "-d", TEST_GET_INNER_DIR, FILE1_PATH, "-o", "dir1"],
        ],
    )
    def test_paths_list_len_error(self, argv: List[str], capsys: pytest.CaptureFixture) -> None:
        self._set_monkeypatch_argv(argv)
        parse_args: Union[argparse.Namespace, None] = None
        with pytest.raises(SystemExit) as excinfo:
            parse_args = get_parser()
        assert parse_args is None
        self._assert_excinfo_expected(excinfo)
        self._assert_err_message_in_outerr(PATHS_LIST_LEN_ERROR, capsys)

    @pytest.mark.parametrize(
        "argv, nonexisting_path",
        [
            (
                ["script.py", "-e", "nonexisting_file1.txt", FILE2_PATH, "-o", "output_file1.txt", "output_file2.txt"],
                "nonexisting_file1.txt",
            ),
            (
                ["script.py", "-d", FILE1_PATH, "nonexisting_dir", "-o", "output_file1.txt", "output_dir"],
                "nonexisting_dir",
            ),
        ],
    )
    def test_input_path_not_found_error(
        self, argv: List[str], nonexisting_path: str, capsys: pytest.CaptureFixture
    ) -> None:
        self._set_monkeypatch_argv(argv)
        parse_args: Union[argparse.Namespace, None] = None
        with pytest.raises(SystemExit) as excinfo:
            parse_args = get_parser()
        assert parse_args is None
        self._assert_excinfo_expected(excinfo)
        self._assert_err_message_in_outerr(PATH_NOT_FOUND_ERROR.format(nonexisting_path), capsys)

    def _assert_excinfo_expected(
            self, 
            excinfo: pytest.ExceptionInfo, 
            expected_code: int = 1, 
            expected_type: Exception = SystemExit
        ) -> None:
        assert excinfo.type == expected_type
        assert excinfo.value.code == expected_code
