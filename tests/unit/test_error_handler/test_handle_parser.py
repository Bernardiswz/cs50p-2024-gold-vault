import pytest
from .error_handler_utils import error_message_in_outerr, excinfo_expected, raise_sys_exit_and_get_excinfo
from gvault.error_handling.type import ErrorHandler  # type: ignore
from gvault.error_handling import ErrorHandlerFactory  # type: ignore
from gvault.error_handling.exceptions.parser_exceptions import (  # type: ignore
    PathsListLenError,
    PathNotFoundError,
    InvalidPathTypeError,
)
from gvault.error_handling.messages.parser_messages import (  # type: ignore
    USAGE,
    PATHS_LIST_LEN_ERROR,
    PATH_NOT_FOUND_ERROR,
    INVALID_PATH_TYPE_ERROR,
)


__all__ = ["TestHandleParser"]


class TestHandleParser:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.error_handler: ErrorHandler = ErrorHandlerFactory.create_handler()

    @pytest.mark.parametrize(
        "parser_exception_instance, message",
        [
            (PathsListLenError(), PATHS_LIST_LEN_ERROR),
            (PathNotFoundError("path"), PATH_NOT_FOUND_ERROR.format("path")),
            (InvalidPathTypeError("path"), INVALID_PATH_TYPE_ERROR.format("path")),
        ],
    )
    def test_handle_parser_exception(
        self, parser_exception_instance: Exception, message: str, capsys: pytest.CaptureFixture
    ) -> None:
        excinfo: pytest.ExceptionInfo = raise_sys_exit_and_get_excinfo(
            self.error_handler.handle_parser_exception, parser_exception_instance
        )
        assert excinfo_expected(excinfo)
        assert error_message_in_outerr(capsys, USAGE, message)
