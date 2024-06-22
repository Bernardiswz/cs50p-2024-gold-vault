import sys
from .error_messages import (
    INVALID_PATH_TYPE_ERROR,
    PATHS_LIST_LEN_ERROR,
    PATH_NOT_FOUND_ERROR,
    USAGE
)


__all__ = ["ErrorHandler"]


class ErrorHandler:
    @staticmethod
    def _parser_exit(message: str) -> None:
        print(USAGE)
        if message:
            print(message)
        sys.exit(1)

    def handle_invalid_path_type(self, path: str) -> None:
        self._parser_exit(INVALID_PATH_TYPE_ERROR.format(path))

    def handle_paths_list_len_error(self) -> None:
        self._parser_exit(PATHS_LIST_LEN_ERROR)

    def handle_path_not_found(self, path: str) -> None:
        self._parser_exit(PATH_NOT_FOUND_ERROR.format(path))
