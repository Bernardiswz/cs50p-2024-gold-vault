from typing import Any, Dict
import pytest
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.padding import PaddingContext
from cryptography.hazmat.primitives.ciphers import Cipher
from gvault.crypto.utils.crypto_utils import (  # type: ignore
    decrypt_data,
    derive_key,
    encrypt_data,
    get_cipher,
    get_padder,
)


__all__ = ["TestCryptoUtils"]


class TestCryptoUtils:
    @pytest.fixture
    def common_data(self) -> Dict[str, Any]:
        password: str = "securepassword"
        salt: bytes = b"salt1234"
        iv: bytes = b"iv12345678901234"
        file_data: bytes = b"Test data for encryption"
        key: bytes = derive_key(password, salt)
        return {"password": password, "salt": salt, "iv": iv, "file_data": file_data, "key": key}

    def test_derive_key(self, common_data: Dict[str, Any]) -> None:
        derived_key: bytes = derive_key(common_data["password"], common_data["salt"])
        assert isinstance(derived_key, bytes)
        assert len(derived_key) == 32

    def test_encrypt_data(self, common_data: Dict[str, Any]) -> None:
        encrypted_data = encrypt_data(common_data["file_data"], common_data["key"], common_data["iv"])
        assert isinstance(encrypted_data, bytes)
        assert encrypted_data != common_data["file_data"]  # Ensure data is encrypted

    def test_decrypt_data(self, common_data: Dict[str, Any]) -> None:
        encrypted_data: bytes = encrypt_data(common_data["file_data"], common_data["key"], common_data["iv"])
        decrypted_data: bytes = decrypt_data(encrypted_data, common_data["key"], common_data["iv"])
        assert decrypted_data == common_data["file_data"]

    def test_get_cipher(self, common_data) -> None:
        cipher: Cipher = get_cipher(common_data["key"], common_data["iv"])
        assert isinstance(cipher, Cipher)

    def test_get_padder(self) -> None:
        padder: PaddingContext = get_padder()
        assert isinstance(padder, padding.PKCS7)
