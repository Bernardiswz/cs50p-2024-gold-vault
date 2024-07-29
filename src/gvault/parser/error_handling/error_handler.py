import sys
from .error_messages import USAGE
from .parser_exceptions import PathsListLenError, PathNotFoundError, InvalidPathTypeError


__all__ = ["ErrorHandler"]


class ErrorHandler:
    @staticmethod
    def _parser_exit(message: str = "") -> None:
        print(USAGE)
        if message:
            print(message)
        sys.exit(1)

    def handle_invalid_path_type(self, invalid_path_type_err: InvalidPathTypeError) -> None:
        self._parser_exit(invalid_path_type_err.message)

    def handle_paths_list_len_error(self, paths_list_len_error: PathsListLenError) -> None:
        self._parser_exit(paths_list_len_error.message)

    def handle_path_not_found(self, path_not_found_error: PathNotFoundError) -> None:
        self._parser_exit(path_not_found_error.message)
