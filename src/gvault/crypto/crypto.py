import argparse
from getpass import getpass
import os
from typing import List
from .decrypt import decrypt_file
from .encrypt import encrypt_file
from .utils.file_utils import confirm_overwrite_path
from .utils import LinkProcessor


__all__ = ["Crypto"]


class Crypto:
    def __init__(self, parse_args: argparse.Namespace) -> None:
        self.parse_args: argparse.Namespace = parse_args
        self.link_processor: LinkProcessor = LinkProcessor()

    def process_paths(self) -> None:
        for input_path, output_path in zip(self.parse_args.input_paths, self.parse_args.output_paths):
            self._process_path(input_path, output_path)

    def _process_path(self, input_path: str, output_path: str) -> None:
        input_path_type: str = self._get_path_type(input_path)
        if not self._should_write_output_path(output_path):
            return
        match input_path_type:
            case "file":
                self._process_file(input_path, output_path)
            case "directory":
                self._process_dir(input_path, output_path)
            case "symlink":
                self._process_path(self._get_link(input_path), output_path)
            case _:
                return

    def _get_path_type(self, path: str) -> str:
        if os.path.isfile(path):
            return "file"
        elif os.path.islink(path):
            return "symlink"
        elif os.path.isdir(path):
            return "directory"
        else:
            return "unknown"

    def _should_write_output_path(self, path: str) -> bool:
        if os.path.exists(path):
            return self._confirm_overwrite_path(path)
        return True    

    def _confirm_overwrite_path(self, path: str) -> bool:
        return confirm_overwrite_path(path)

    def _get_link(self, link_path: str) -> str:
        return self._get_link_path(link_path)

    def _get_link_path(self, link_path: str) -> str:
        self.link_processor.get_link_path(link_path)

    def _process_file(self, input_file_path: str, output_file_path: str) -> None:
        if self.parse_args.encrypt:
            self._encrypt_file(input_file_path, output_file_path, self._get_password())
        elif self.parse_args.decrypt:
            self._decrypt_file(input_file_path, output_file_path, self._get_password())

    def _encrypt_file(self, input_file_path: str, output_file_path: str) -> None:
        encrypt_file(input_file_path, output_file_path, self._get_password())

    def _decrypt_file(self, input_file_path: str, output_file_path: str) -> None:
        decrypt_file(input_file_path, output_file_path, self._get_password())

    def _get_password(self) -> str:
        return getpass("Enter your password:")

    def _process_dir(self, input_dir: str, output_dir: str) -> None:
        for root, _, files in os.walk(input_dir):
            relative_path: str = os.path.relpath(root, input_dir)
            output_root: str = os.path.join(output_dir, relative_path)
            if not self._should_write_output_path(output_root):
                continue
            self._make_output_dir(output_root)
            self._process_dir_child_items(files, root, output_root)

    def _make_output_dir(self, path: str) -> None:
        os.makedirs(path)

    def _process_dir_child_items(self, files: List[str], root: str, output_root: str) -> None:
        for file_name in files:
            input_file_path: str = os.path.join(root, file_name)
            output_file_path: str = os.path.join(output_root, file_name)
            self._process_path(input_file_path, output_file_path)
