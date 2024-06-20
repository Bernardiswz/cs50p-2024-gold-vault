# Create dedicated module to error messages
PATHS_LIST_LEN_ERROR: str = "Error: Lengths of input and output paths list must match."
PATH_NOT_FOUND_ERROR: str = "Error: Path '{}' does not exist."

class PathsListLenError(Exception):
    def __init__(self, message=PATHS_LIST_LEN_ERROR):
        self.message: str = PATHS_LIST_LEN_ERROR
        super().__init__(message)


class PathNotFoundError(Exception):
    def __init__(self, path: str, message=PATH_NOT_FOUND_ERROR):
        self.message: str = PATH_NOT_FOUND_ERROR
        super().__init__(message.format(path))
