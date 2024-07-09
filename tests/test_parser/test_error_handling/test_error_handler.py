import pytest
from typing import List
from _pytest.capture import CaptureResult # Type hinting
from gvault.parser.types import ErrorHandler
from gvault.parser.factories import (
    ErrorHandlerFactory
)
from gvault.parser.error_handling.error_messages import (
    PATHS_LIST_LEN_ERROR,
    PATH_NOT_FOUND_ERROR,
    INVALID_PATH_TYPE_ERROR,
    USAGE
)


class TestErrorHandler:
    @pytest.fixture(autouse=True)
    def setup(self, error_handler: ErrorHandler) -> None:
        self.error_handler: ErrorHandler = error_handler

    @pytest.fixture
    def error_handler(self) -> ErrorHandler:
        return ErrorHandlerFactory.create_handler()
          
    def test_expected_exit_status(self, capsys: pytest.CaptureFixture):
        with pytest.raises(SystemExit) as excinfo:
            self.error_handler._parser_exit()
        assert excinfo.type == SystemExit
        assert excinfo.value.code == 1

        captured: CaptureResult = capsys.readouterr()
        assert USAGE in captured.out

    @pytest.mark.parametrize("path", ["path_1.py", "path_2/file_1.py"])
    def test_handle_invalid_path_type(self, capsys: pytest.CaptureFixture, path: str):
        with pytest.raises(SystemExit):
            self.error_handler.handle_invalid_path_type(INVALID_PATH_TYPE_ERROR.format(path))
            captured: CaptureResult = capsys.readouterr()
            assert INVALID_PATH_TYPE_ERROR.format(path) in captured

    def test_handle_paths_list_len(self, capsys: pytest.CaptureFixture):
        with pytest.raises(SystemExit):
            self.error_handler.handle_paths_list_len_error()
            captured: CaptureResult = capsys.readouterr()
            assert PATHS_LIST_LEN_ERROR in captured

    @pytest.mark.parametrize("path", ["path_1.py", "path_2/file_1.py"])
    def test_handle_path_not_found(self, capsys:pytest.CaptureFixture, path: str):
        with pytest.raises(SystemExit):
            self.error_handler.handle_path_not_found(PATH_NOT_FOUND_ERROR.format(path))
            captured: CaptureResult = capsys.readouterr()
            assert PATH_NOT_FOUND_ERROR.format(path) in captured
