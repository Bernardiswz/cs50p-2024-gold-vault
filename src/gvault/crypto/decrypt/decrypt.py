"""
This module contains the functions to perform decryption on files encrypted by the functions and functionality of the
'encrypt' package/module.
"""

from typing import Tuple
from ..utils.crypto_utils import derive_key, decrypt_data
from ..utils.file_utils import read_file, write_file
from gvault.error_handling.exceptions.crypto_exceptions import DecryptionError  # type: ignore


__all__ = ["decrypt_file, get_salt_iv, get_ciphertext"]


def decrypt_file(input_path: str, output_path: str, password: str) -> None:
    """
    Attempt decryption on file given as 'input_path' and write it to 'output_path' using given password.

    Read file content, extract the salt and iv from the encrypted data of the file, retrieve ciphertext and
    attempt to decrypt data by calling 'decrypt_data', if sucessful, write its content to the output_path, else
    DecryptionError raised.

    Args:
        input_path (str): Input path to the file to be decrypted.
        output_path (str): Output path to the now decrypted file (if sucessful) to be written to.
        password (str): Password to be derived to key and attempted to decrypt data.

    Raises:
        DecryptionError: Raised when ValueError is raised, as implies a error in decryption of file.
    """
    encrypted_data: bytes = read_file(input_path)
    salt, iv = get_salt_iv(encrypted_data)
    ciphertext: bytes = get_ciphertext(encrypted_data)
    key: bytes = derive_key(password, salt)
    try:
        decrypted_data: bytes = decrypt_data(ciphertext, key, iv)
        write_file(output_path, decrypted_data)
    except ValueError:
        raise DecryptionError(input_path)


def get_salt_iv(encrypted_data: bytes) -> Tuple[bytes, bytes]:
    """
    Extracts the salt and iv from the encrypted data of a file.

    Args:
        encrypted_data (bytes): Data from the encrypted file.
    """
    salt: bytes = encrypted_data[:16]
    iv: bytes = encrypted_data[16:32]
    return salt, iv


def get_ciphertext(encrypted_data: bytes) -> bytes:
    """
    Extracts the ciphertext of the encrypted_data, skipping the indexes that contain salt and iv.

    Args:
        encrypted_data (bytes): Data from the encrypted file.

    Returns:
        encrypted_data[32:] (bytes): Plain ciphertext of the encrypted file data without the salt or iv.
    """
    return encrypted_data[32:]
