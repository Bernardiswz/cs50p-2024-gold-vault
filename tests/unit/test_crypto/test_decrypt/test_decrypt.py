import os
import pytest
from typing import Any, Generator, Set
from gvault.crypto.decrypt import decrypt_file, get_salt_iv, get_ciphertext  # type: ignore
from gvault.crypto.encrypt import encrypt_file  # type: ignore
from gvault.crypto.utils.file_utils import read_file, write_file  # type: ignore
from gvault.error_handling.exceptions.crypto_exceptions import DecryptionError  # type: ignore


__all__ = ["TestDecrypt"]


ENCRYPTION_PASSWORD: str = "1965917"


class DecryptFilesSetup:
    TEST_DIR: str = "decrypt dir"
    SAMPLE_FILE_PATH: str = os.path.join(TEST_DIR, "file.txt")
    SAMPLE_FILE_CONTENT: bytes = b"some content"
    ENCRYPTED_FILE_PATH: str = os.path.join(TEST_DIR, "encrypted_file.txt")
    DECRYPTED_FILE_PATH: str = os.path.join(TEST_DIR, "decrypted_file.txt")
    FILE_PATHS: Set[str] = {SAMPLE_FILE_PATH, ENCRYPTED_FILE_PATH, DECRYPTED_FILE_PATH}

    def setup(self) -> None:
        self._make_test_dir()
        self._write_sample_file()
        self._encrypt_sample_file()

    def _make_test_dir(self) -> None:
        if not os.path.exists(self.TEST_DIR):
            os.makedirs(self.TEST_DIR, exist_ok=True)

    def _write_sample_file(self) -> None:
        write_file(self.SAMPLE_FILE_PATH, self.SAMPLE_FILE_CONTENT)

    def _encrypt_sample_file(self) -> None:
        encrypt_file(self.SAMPLE_FILE_PATH, self.ENCRYPTED_FILE_PATH, ENCRYPTION_PASSWORD)

    def teardown(self) -> None:
        self._remove_test_files()
        self._remove_test_dir()

    def _remove_test_files(self) -> None:
        for file_path in self.FILE_PATHS:
            if os.path.exists(file_path):
                os.remove(file_path)

    def _remove_test_dir(self) -> None:
        if os.path.exists(self.TEST_DIR):
            os.rmdir(self.TEST_DIR)


class TestDecrypt:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> Generator[None, Any, None]:
        self.password: str = "somepassword"
        self.setup: DecryptFilesSetup = DecryptFilesSetup()
        self.setup.setup()
        yield
        self.setup.teardown()

    def test_decrypt(self) -> None:
        # Correct password decrypts file sucessfully
        decrypt_file(self.setup.ENCRYPTED_FILE_PATH, self.setup.DECRYPTED_FILE_PATH, ENCRYPTION_PASSWORD)
        decrypted_sample_file_content: bytes = read_file(self.setup.DECRYPTED_FILE_PATH)
        assert self.setup.SAMPLE_FILE_CONTENT == decrypted_sample_file_content

    def test_decrypt_invalid_password(self) -> None:
        # Invalid password expected to raise decryption error
        with pytest.raises(DecryptionError):
            decrypt_file(self.setup.ENCRYPTED_FILE_PATH, self.setup.DECRYPTED_FILE_PATH, "19921124")

    def test_get_salt_iv(self) -> None:
        encrypted_file_data: bytes = read_file(self.setup.ENCRYPTED_FILE_PATH)
        salt, iv = get_salt_iv(encrypted_file_data)
        assert salt == encrypted_file_data[:16]
        assert iv == encrypted_file_data[16:32]

    def test_get_ciphertext(self) -> None:
        encrypted_file_data: bytes = read_file(self.setup.ENCRYPTED_FILE_PATH)
        ciphertext: bytes = get_ciphertext(encrypted_file_data)
        assert ciphertext == encrypted_file_data[32:]
