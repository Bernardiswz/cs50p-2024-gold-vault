import hashlib
import os
from typing import Tuple
from cryptography.hazmat.primitives.ciphers import (
    AEADEncryptionContext,
    AEADDecryptionContext,
    algorithms,
    Cipher,
    modes
)
from cryptography.hazmat.backends import default_backend


__all__ = ["derive_key", "encrypt_data", "decrypt_data"]


def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()


def encrypt_data(data: bytes, key: bytes) -> Tuple[bytes, bytes]:
    iv: bytes = os.urandom(16)  # Generate a random IV
    cipher: Cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor: AEADEncryptionContext = cipher.encryptor()
    encrypted_data: bytes = encryptor.update(data) + encryptor.finalize()
    return encrypted_data, iv


def decrypt_data(encrypted_data: bytes, key: bytes, iv: bytes) -> bytes:
    cipher: Cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor: AEADDecryptionContext = cipher.decryptor()
    decrypted_data: bytes = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_data
