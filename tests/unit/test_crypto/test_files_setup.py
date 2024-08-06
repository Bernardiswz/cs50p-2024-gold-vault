import os
from typing import List


__all__ = ["TestFilesSetup"]


class TestFilesSetup:
    TEST_DIR: str = "test_dir"
    TEST_FILE: str = os.path.join(TEST_DIR, "test_file.txt")
    OUTPUT_TEST_FILE: str = os.path.join(TEST_DIR, "output_file.txt")
    FILE_PATHS: List[str] = [TEST_FILE, OUTPUT_TEST_FILE]

    def setup(self) -> None:
        self._make_test_dirs()
        self._write_test_file()

    def _make_test_dirs(self) -> None:
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
