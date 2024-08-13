"""
Contains utility functions related to writing, reading of files and confirmation of overwriting of paths that
already exist.
"""

__all__ = ["confirm_overwrite_path", "read_file", "write_file"]


def read_file(filepath: str) -> bytes:
    """
    Opens 'filepath' in 'rb' mode and returns its data.

    Args:
        filepath (str).

    Returns:
        (bytes): File data.
    """
    with open(filepath, "rb") as file:
        return file.read()


def write_file(filepath: str, data: bytes) -> None:
    """
    Write 'data' to 'filepath' in 'wb' mode.

    Args:
        filepath (str).
        data (bytes): Data to be written on 'filepath'.
    """
    with open(filepath, "wb") as file:
        file.write(data)


def confirm_overwrite_path(path: str) -> bool:
    """
    Prompts use for confirmation to whether a path should be overwrited with an given output path if it already exists.
    Returns true if answer is 'y' or 'yes'.

    Args:
        path (str).

    Returns:
        (bool): User response is 'y' or 'yes'.
    """
    response: str = input(f"Path '{path}' already exists, overwrite? [y/n]").lower()
    return response in {"y", "yes"}
