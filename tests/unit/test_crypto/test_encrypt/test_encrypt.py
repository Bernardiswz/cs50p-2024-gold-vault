import pytest
import os
from typing import Any, Generator
from unittest.mock import patch, mock_open, MagicMock
from gvault.crypto.encrypt import encrypt_file, generate_salt_iv # type: ignore



class Mocks:
    def __init__(self) -> None:
        self.mock_urandom: MagicMock = patch("os.urandom")
        self.mock_generate_salt_iv: MagicMock = patch("gvault.crypto.encrypt.generate_salt_iv")
        self.mock_derive_key: MagicMock = patch("gvault.crypto.utils.crypto_utils.derive_key")
        self.mock_read_file: MagicMock = patch("gvault.crypto.file_utils.read_file")
        self.mock_encrypt_data: MagicMock = patch("gvault.crypto.utils.crypto_utils.encrypt_data")
        self.mock_write_file: MagicMock = patch("gvault.crypto.file_utils.write_file")

    def stop_patches(self) -> None:
        patch.stopall()


@pytest.fixture
def patches() -> Generator[Mocks, Any, None]:
    mocks: Mocks = Mocks()
    yield mocks
    mocks.stop_patches()


class TestCryptoUtils:
    def test_generate_salt_iv(self, patches: Mocks) -> None:
        patches.mock_urandom.side_effect = [b"salt_bytes", b"iv_byte"]
        salt, iv = generate_salt_iv()
        assert salt == b"salt_bytes"
        assert iv == b"iv_bytes"
        assert len(salt) == 16
        assert len(iv) == 16

    @pytest.mark.skip
    def test_encrypt_file(
        self, 
        mock_generate_salt_iv, 
        mock_derive_key, 
        mock_read_file, 
        mock_encrypt_data, 
        mock_write_file
        ) -> None:
        mock_generate_salt_iv.return_value = (b"salt_bytes", b"iv_bytes")
        mock_derive_key.return_value = b"derived_key"
        mock_read_file.return_value = b"file_data"
        mock_encrypt_data.return_value = b"encrypted_data"

        input_path = "input.txt"
        output_path = "output.txt"
        password = "password"

        encrypt_file(input_path, output_path, password)

        # Verify that the functions were called with the expected arguments
        mock_generate_salt_iv.assert_called_once()
        mock_derive_key.assert_called_once_with(password, b'salt_bytes')
        mock_read_file.assert_called_once_with(input_path)
        mock_encrypt_data.assert_called_once_with(b'file_data', b'derived_key', b'iv_bytes')
        mock_write_file.assert_called_once_with(output_path, b'salt_bytes' + b'iv_bytes' + b'encrypted_data')
