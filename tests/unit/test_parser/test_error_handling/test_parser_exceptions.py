import pytest
from gvault.error_handling.messages.parser_messages import (  # type: ignore
    PATHS_LIST_LEN_ERROR,
    PATH_NOT_FOUND_ERROR,
    INVALID_PATH_TYPE_ERROR,
)
from gvault.error_handling.exceptions.parser_exceptions import (  # type: ignore
    PathsListLenError,
    PathNotFoundError,
    InvalidPathTypeError,
)


__all__ = ["TestParserExceptions"]


class TestParserExceptions:
    def test_paths_list_len_error(self) -> None:
        with pytest.raises(PathsListLenError) as excinfo:
            raise PathsListLenError()
        exception_instance: PathsListLenError = excinfo.value
        assert exception_instance.message == PATHS_LIST_LEN_ERROR

    @pytest.mark.parametrize("path", ["path_1.py", "path_2/file_1.py"])
    def test_path_not_found_error(self, path: str) -> None:
        with pytest.raises(PathNotFoundError) as excinfo:
            raise PathNotFoundError(path)
        exception_instance: PathsListLenError = excinfo.value
        assert exception_instance.message == PATH_NOT_FOUND_ERROR.format(path)

    @pytest.mark.parametrize("path", ["path_1.py", "path_2/file_1.py"])
    def test_invalid_path_type_error(self, path: str) -> None:
        with pytest.raises(InvalidPathTypeError) as excinfo:
            raise InvalidPathTypeError(path)
        exception_instance: PathsListLenError = excinfo.value
        assert exception_instance.message == INVALID_PATH_TYPE_ERROR.format(path)
