import pytest
from _pytest.capture import CaptureResult  # Type hinting
from gvault.parser.parser_types import ErrorHandler  # type: ignore
from gvault.parser.factories import ErrorHandlerFactory  # type: ignore
from gvault.parser.error_handling.error_messages import (  # type: ignore
    PATHS_LIST_LEN_ERROR,
    PATH_NOT_FOUND_ERROR,
    INVALID_PATH_TYPE_ERROR,
    USAGE,
)


__all__ = ["TestErrorHandler"]


class TestErrorHandler:
    @pytest.fixture(autouse=True)
    def setup_method(self, error_handler: ErrorHandler) -> None:
        self.error_handler_instance: ErrorHandler = error_handler

    @pytest.fixture
    def error_handler(self) -> ErrorHandler:
        return ErrorHandlerFactory.create_handler()

    def assert_err_message_in_outerr(self, error_message: str, capsys: pytest.CaptureFixture) -> None:
        captured: CaptureResult = capsys.readouterr()
        assert error_message in captured.out or error_message in captured.err

    def test_expected_exit_status(self, capsys: pytest.CaptureFixture) -> None:
        with pytest.raises(SystemExit) as excinfo:
            self.error_handler_instance._parser_exit()

        assert excinfo.type == SystemExit
        assert excinfo.value.code == 1
        self.assert_err_message_in_outerr(USAGE, capsys)

    @pytest.mark.parametrize("path", ["path_1.py", "path_2/file_1.py"])
    def test_handle_invalid_path_type(self, capsys: pytest.CaptureFixture, path: str) -> None:
        with pytest.raises(SystemExit):
            self.error_handler_instance.handle_invalid_path_type(INVALID_PATH_TYPE_ERROR.format(path))
        self.assert_err_message_in_outerr(INVALID_PATH_TYPE_ERROR.format(path), capsys)

    def test_handle_paths_list_len(self, capsys: pytest.CaptureFixture) -> None:
        with pytest.raises(SystemExit):
            self.error_handler_instance.handle_paths_list_len_error()
        self.assert_err_message_in_outerr(PATHS_LIST_LEN_ERROR, capsys)

    @pytest.mark.parametrize("path", ["path_1.py", "path_2/file_1.py"])
    def test_handle_path_not_found(self, capsys: pytest.CaptureFixture, path: str) -> None:
        with pytest.raises(SystemExit):
            self.error_handler_instance.handle_path_not_found(PATH_NOT_FOUND_ERROR.format(path))
        self.assert_err_message_in_outerr(PATH_NOT_FOUND_ERROR.format(path), capsys)
