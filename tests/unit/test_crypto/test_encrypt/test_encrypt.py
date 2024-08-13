import os
import pytest
from typing import Any, Dict, Generator, Set
from gvault.crypto.encrypt import encrypt_file  # type: ignore
from gvault.crypto.utils.file_utils import read_file  # type: ignore


__all__ = ["TestEncrypt"]


class EncryptFilesSetup:
    TEST_DIR: str = "encrypt_dir"
    TEST_FILE: str = os.path.join(TEST_DIR, "test_file.txt")
    OUTPUT_TEST_FILE: str = os.path.join(TEST_DIR, "output_file.txt")
    FILE_PATHS: Set[str] = {TEST_FILE, OUTPUT_TEST_FILE}

    def setup(self) -> None:
        self._make_test_dir()
        self._write_test_file()

    def _make_test_dir(self) -> None:
        os.makedirs(self.TEST_DIR, exist_ok=True)

    def _write_test_file(self) -> None:
        with open(self.TEST_FILE, "w") as file:
            file.write("Some content")

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


class TestEncrypt:
    @pytest.fixture
    def paths(self) -> Generator[Any, None, None]:
        setup: EncryptFilesSetup = EncryptFilesSetup()
        setup.setup()
        yield {"dir": setup.TEST_DIR, "input_file": setup.TEST_FILE, "output_file": setup.OUTPUT_TEST_FILE}
        setup.teardown()

    def test_encrypt_file(self, paths: Dict[str, str]):
        # Call the function under test
        input_file_path: str = paths["input_file"]
        output_file_path: str = paths["output_file"]
        password: str = "somepassword"
        input_file_data: bytes = read_file(input_file_path)
        encrypt_file(input_file_path, output_file_path, password)
        output_file_data: bytes = read_file(output_file_path)
        assert input_file_data != output_file_data
        assert len(output_file_data) > len(input_file_data)
