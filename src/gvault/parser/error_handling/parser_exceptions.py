from .error_messages import (
    PATHS_LIST_LEN_ERROR,
    PATH_NOT_FOUND_ERROR,
    INVALID_PATH_TYPE_ERROR
)


__all__ = [
    "PathsListLenError",
    "PathNotFoundError",
    "InvalidPathTypeError"
]


class PathsListLenError(Exception):
    def __init__(self):
        self.message: str = PATHS_LIST_LEN_ERROR
        super().__init__(self.message)


class PathNotFoundError(Exception):
    def __init__(self, path: str):
        self.message: str = PATH_NOT_FOUND_ERROR
        super().__init__(self.message.format(path))


class InvalidPathTypeError(Exception):
    def __init__(self, path: str):
        self.message: str = INVALID_PATH_TYPE_ERROR
        super().__init__(self.message.format(path))
