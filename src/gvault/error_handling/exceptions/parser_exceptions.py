"""
Contains custom exceptions to be used on Parser package.
"""

from ..messages.parser_messages import PATHS_LIST_LEN_ERROR, PATH_NOT_FOUND_ERROR, INVALID_PATH_TYPE_ERROR


__all__ = ["PathsListLenError", "PathNotFoundError", "InvalidPathTypeError"]


class PathsListLenError(Exception):
    """
    Raised when parse_args parameters of 'input_paths' and 'output_paths' are of different lenghts.
    """

    def __init__(self) -> None:
        """
        Initializes super class and declares instance variable message.
        """
        self.message: str = PATHS_LIST_LEN_ERROR
        super().__init__(self.message)


class PathNotFoundError(Exception):
    """
    Raised when any path of parse_args's 'input_paths' doesn't exist.
    """

    def __init__(self, path: str) -> None:
        """
        Initializes path and message instance variables referent to the error and path that is source of the problem.

        Args:
            path (str).
        """
        self.path: str = path
        self.message: str = PATH_NOT_FOUND_ERROR.format(path)
        super().__init__(self.message)


class InvalidPathTypeError(Exception):
    """
    Raised when any given path is of a invalid type (not file, link or dir).
    """

    def __init__(self, path: str) -> None:
        """
        Intializes path and message instance variables with information regarding the error.

        Args:
            path (str).
        """
        self.path: str = path
        self.message: str = INVALID_PATH_TYPE_ERROR.format(path)
        super().__init__(self.message)
