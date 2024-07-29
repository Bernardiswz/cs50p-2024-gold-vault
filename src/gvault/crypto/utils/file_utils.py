__all__ = ["confirm_overwrite_path", "read_file", "write_file"]


def read_file(filepath: str) -> bytes:
    with open(filepath, "rb") as file:
        return file.read()


def write_file(filepath: str, data: bytes) -> None:
    with open(filepath, "wb") as file:
        file.write(data)


def confirm_overwrite_path(path: str) ->  bool:
    response: str = input(f"Path '{path}' already exists, overwrite? [y/n]").lower()
    return response in {"y", "yes"}
