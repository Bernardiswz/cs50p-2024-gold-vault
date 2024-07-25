import os
from ..utils.crypto_utils import derive_key, encrypt_data
from ..utils.file_utils import read_file, write_file


def encrypt_file(input_path: str, output_path: str, password: str) -> None:
    salt: bytes = os.urandom(16)  # Generate a random salt
    key: bytes = derive_key(password, salt)
    iv: bytes = os.urandom(16)  # Initialization vector for AES
    file_data: bytes = read_file(input_path)
    encrypted_data: bytes = encrypt_data(file_data, key, iv)
    write_file(output_path, salt + iv + encrypted_data)
