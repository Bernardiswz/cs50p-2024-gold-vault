__all__ = ["read_file", "write_file"]


def read_file(filepath: str) -> bytes:
    with open(filepath, 'rb') as file:
        return file.read()


def write_file(filepath: str, data: bytes) -> None:
    with open(filepath, 'wb') as file:
        file.write(data)
