import pytest
from typing import Any, Dict, Generator
from ..test_files_setup import TestFilesSetup
from gvault.crypto.decrypt import ( # type: ignore
    decrypt_file,
    get_salt_iv,
    get_ciphertext
)
from gvault.crypto.encrypt import encrypt_file
from gvault.crypto.utils.file_utils import read_file
from gvault.error_handling.exceptions.crypto_exceptions import DecryptionError # type: ignore


class TestDecrypt:
    @pytest.fixture(autouse=True)
    def setup_method(self, paths: Dict[str, str]) -> None:
        self.input_file_path: str = paths["input_file"]
        self.output_file_path: str = paths["output_file"]
        self.password: str = "somepassword"
        self.input_file_data: bytes = read_file(self.input_file_path)


    @pytest.fixture
    def paths(self) -> Generator[Any, None, None]:
        setup: TestFilesSetup = TestFilesSetup()
        setup.setup()
        yield {"dir": setup.TEST_DIR, "input_file": setup.TEST_FILE, "output_file": setup.OUTPUT_TEST_FILE}
        setup.teardown()

    def test_decrypt(self) -> None:
        encrypt_file(self.input_file_path, self.output_file_path, self.password)
        decrypt_file(self)