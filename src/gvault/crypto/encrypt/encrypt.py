import os
from typing import Tuple
from ..utils.crypto_utils import derive_key, encrypt_data
from ..utils.file_utils import read_file, write_file


__all__ = ["encrypt_file", "generate_salt_iv"]


def encrypt_file(input_path: str, output_path: str, password: str) -> None:
    salt, iv = generate_salt_iv()
    key: bytes = derive_key(password, salt)
    file_data: bytes = read_file(input_path)
    encrypted_data: bytes = encrypt_data(file_data, key, iv)
    write_file(output_path, salt + iv + encrypted_data)


def generate_salt_iv() -> Tuple[bytes, bytes]:
    salt: bytes = os.urandom(16)
    iv: bytes = os.urandom(16)
    return salt, iv
