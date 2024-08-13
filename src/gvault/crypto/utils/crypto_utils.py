"""
This module contains utility functions to be used throughout the crypto package.
"""

from typing import Any
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.padding import PaddingContext, PKCS7
from cryptography.hazmat.primitives.ciphers import AEADDecryptionContext, algorithms, Cipher, CipherContext, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


__all__ = ["decrypt_data", "derive_key", "encrypt_data", "get_cipher", "get_padder"]


def derive_key(password: str, salt: bytes, iterations: int = 100000) -> bytes:
    """
    Derives password and salt into a key to use for encrption and decryption of files.

    Args:
        password (str).
        salt (bytes).
        iterations (int): How many interations on cryptography algorithm/key derivation.

    Returns:
        bytes: Derived key from password and salt.
    """
    kdf: Any = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations, backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_data(file_data: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Encrypts 'file_data' (bytes) using of 'key' and 'iv' and returns the encrypted data.

    Calls on get_cipher to get a cipher to apply on the 'file_data' to encryption using 'key' and 'iv', then
    perform padding on the data to ensure consistency and functionality. Then proceed to return the now encrypted data.

    Args:
        file_data (bytes).
        key (bytes).
        iv (bytes).

    Returns:
        ciphertext (bytes): Encrypted data.
    """
    cipher: Cipher = get_cipher(key, iv)
    encryptor: CipherContext = cipher.encryptor()
    padder: PaddingContext = get_padder().padder()  # type: ignore
    padded_data: bytes = padder.update(file_data) + padder.finalize()
    ciphertext: bytes = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext


def decrypt_data(encrypted_data: bytes, key: bytes, iv: bytes) -> bytes:
    """
    Attempts decryption on the 'encrypted_data' through the use of 'key' and 'iv' params. If sucessful, returns
    the decrypted data.

    The cipher is retrieved with get_cipher, then attempts to perform decryption on the file data, unpadds it which was
    necessary in decryption phase, then returns the decrypted data.

    Args:
        encrypted_data (bytes).
        key (bytes).
        iv (bytes).
    """
    cipher: Cipher = get_cipher(key, iv)
    decryptor: AEADDecryptionContext = cipher.decryptor()
    decrypted_padded_data: bytes = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder: PaddingContext = get_padder().unpadder()  # type: ignore
    decrypted_data: bytes = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return decrypted_data


def get_cipher(key: bytes, iv: bytes) -> Cipher:
    """
    Returns a Cipher object using of 'key' and 'iv' params.

    Args:
        key (bytes).
        iv (bytes).

    Returns:
        Cipher: Object of Cipher class with params of 'key' and 'iv'.
    """
    return Cipher(algorithms.AES(key), modes.CBC(iv))


def get_padder() -> PKCS7:
    """
    Returns an object of PKCS7 to apply padding or unpadding on file data.

    Returns:
        padding.PKCS7: Object of PKCS7 class to perform padding and unpadding on data.
    """
    return padding.PKCS7(algorithms.AES.block_size)
