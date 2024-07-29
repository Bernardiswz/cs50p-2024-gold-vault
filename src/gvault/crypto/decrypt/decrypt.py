from typing import Any, Dict, Tuple, Union
from ..error_handling.exceptions import DecryptionError
from ..utils.crypto_utils import derive_key, decrypt_data
from ..utils.file_utils import read_file, write_file


__all__ = ["decrypt_file"]


def decrypt_file(input_path: str, output_path: str, password: str) -> None:
    encrypted_data: bytes = read_file(input_path)
    salt, iv = get_salt_iv(encrypted_data)
    ciphertext: bytes = get_ciphertext(encrypted_data)
    key = derive_key(password, salt)
    try:
        decrypted_data: bytes = decrypt_data(ciphertext, key, iv)
        write_file(output_path, decrypted_data)
    except ValueError:
        raise DecryptionError(input_path)


def get_salt_iv(encrypted_data: bytes) -> Tuple[bytes, bytes]:
    salt: bytes = encrypted_data[:16]
    iv: bytes = encrypted_data[16:32]
    return salt, iv


def get_ciphertext(encrypted_data: bytes) -> bytes:
    return encrypted_data[32:]
