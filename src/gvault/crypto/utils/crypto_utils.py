from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.padding import PaddingContext
from cryptography.hazmat.primitives.ciphers import (
    AEADDecryptionContext,
    algorithms,
    Cipher,
    CipherContext,
    modes
)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


__all__ = ["derive_key", "encrypt_data", "decrypt_data"]


def derive_key(password: str, salt: bytes, iterations: int = 100000) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


def encrypt_data(file_data: bytes, key: bytes, iv: bytes) -> bytes:
    cipher: Cipher = get_cipher(key, iv)
    encryptor: CipherContext = cipher.encryptor()
    padder: PaddingContext = get_padder().padder()
    padded_data: bytes = padder.update(file_data) + padder.finalize()
    ciphertext: bytes = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext


def decrypt_data(encrypted_data: bytes, key: bytes, iv: bytes) -> bytes:
    cipher: Cipher = get_cipher(key, iv)
    decryptor: AEADDecryptionContext = cipher.decryptor()
    decrypted_padded_data: bytes = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder: PaddingContext = get_padder().unpadder()
    decrypted_data: bytes = unpadder.update(decrypted_padded_data) + unpadder.finalize()
    return decrypted_data


def get_cipher(key: bytes, iv: bytes) -> Cipher:
    return Cipher(algorithms.AES(key), modes.CBC(iv))


def get_padder() -> PaddingContext:
    return padding.PKCS7(algorithms.AES.block_size)
