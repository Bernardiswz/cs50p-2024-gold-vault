import os
import pytest
from typing import Any, Dict, Generator
from ..test_files_setup import TestFilesSetup
from gvault.crypto.encrypt import encrypt_file
from gvault.crypto.utils.file_utils import read_file



__all__ = ["TestEncrypt"]




class TestEncrypt:
    @pytest.fixture
    def paths(self) -> Generator[Any, None, None]:
        setup: TestFilesSetup = TestFilesSetup()
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
