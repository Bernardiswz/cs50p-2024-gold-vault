import pytest
from .exception_utils import ExceptionData, exception_attr_is_expected
from gvault.error_handling.exceptions.parser_exceptions import (  # type: ignore
    PathsListLenError,
    PathNotFoundError,
    InvalidPathTypeError,
)
from gvault.error_handling.messages.parser_messages import (  # type: ignore
    PATHS_LIST_LEN_ERROR,
    PATH_NOT_FOUND_ERROR,
    INVALID_PATH_TYPE_ERROR,
)


__all__ = ["TestParserExceptions"]


class TestParserExceptions:
    @pytest.mark.parametrize(
        "exception_data",
        [
            (ExceptionData(PathsListLenError(), "message", PATHS_LIST_LEN_ERROR)),
            (ExceptionData(PathNotFoundError("some/path"), "message", PATH_NOT_FOUND_ERROR.format("some/path"))),
            (ExceptionData(InvalidPathTypeError("some/path"), "message", INVALID_PATH_TYPE_ERROR.format("some/path"))),
        ],
    )
    def test_exception_attr_is_expected(self, exception_data: ExceptionData) -> None:
        assert exception_attr_is_expected(exception_data)
