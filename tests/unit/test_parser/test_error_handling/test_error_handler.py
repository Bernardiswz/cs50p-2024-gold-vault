import pytest
from _pytest.capture import CaptureResult  # Type hinting
from gvault.parser.parser_types import ErrorHandler  # type: ignore
from gvault.parser.factories import ErrorHandlerFactory  # type: ignore
from gvault.parser.error_handling.error_messages import USAGE  # type: ignore
from gvault.parser.error_handling.parser_exceptions import (  # type: ignore
    PathsListLenError,
    PathNotFoundError,
    InvalidPathTypeError,
)


__all__ = ["TestErrorHandler"]


class TestErrorHandler:
    @pytest.fixture(autouse=True)
    def setup_method(self, error_handler: ErrorHandler) -> None:
        self.error_handler_instance: ErrorHandler = error_handler

    @pytest.fixture
    def error_handler(self) -> ErrorHandler:
        return ErrorHandlerFactory.create_handler()

    def _assert_err_message_in_outerr(self, error_message: str, capsys: pytest.CaptureFixture) -> None:
        captured: CaptureResult = capsys.readouterr()
        assert error_message in captured.out or error_message in captured.err

    def test_expected_exit_status(self, capsys: pytest.CaptureFixture) -> None:
        with pytest.raises(SystemExit) as excinfo:
            self.error_handler_instance._parser_exit()
        assert excinfo.type == SystemExit
        assert excinfo.value.code == 1
        self._assert_err_message_in_outerr(USAGE, capsys)

    @pytest.mark.parametrize("path", ["path_1.py", "path_2/file_1.py"])
    def test_handle_invalid_path_type(self, capsys: pytest.CaptureFixture, path: str) -> None:
        invalid_path_type_error: InvalidPathTypeError = InvalidPathTypeError(path)
        with pytest.raises(SystemExit):
            self.error_handler_instance.handle_invalid_path_type(invalid_path_type_error)
        self._assert_err_message_in_outerr(invalid_path_type_error.message, capsys)

    def test_handle_paths_list_len(self, capsys: pytest.CaptureFixture) -> None:
        paths_list_len_error: PathsListLenError = PathsListLenError()
        with pytest.raises(SystemExit):
            self.error_handler_instance.handle_paths_list_len_error(paths_list_len_error)
        self._assert_err_message_in_outerr(paths_list_len_error.message, capsys)

    @pytest.mark.parametrize("path", ["path_1.py", "path_2/file_1.py"])
    def test_handle_path_not_found(self, capsys: pytest.CaptureFixture, path: str) -> None:
        path_not_found_error: PathNotFoundError = PathNotFoundError(path)
        with pytest.raises(SystemExit):
            self.error_handler_instance.handle_path_not_found(path_not_found_error)
        self._assert_err_message_in_outerr(path_not_found_error.message, capsys)
