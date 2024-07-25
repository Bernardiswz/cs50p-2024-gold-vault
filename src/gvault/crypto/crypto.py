import argparse
import os
from unittest.util import strclass
from .decrypt import decrypt_file
from .encrypt import encrypt_file
from .utils import LinkProcessor, PasswordHandler


class Crypto:
    def __init__(self, parse_args: argparse.Namespace) -> None:
        self.parse_args: argparse.Namespace = parse_args

    def process_paths(self) -> None:
        for input_path, output_path in zip(self.parse_args.input_paths, self.parse_args.output_paths):
            self._process_path(input_path, output_path)

    def _process_path(self, input_path: str, output_path: strclass) -> None:        
        if os.path.islink(input_path):
            input_path: str = self._process_link(input_path)
        if os.path.isfile(input_path):
            self._process_file(input_path, output_path)
        elif os.path.isdir(input_path):
            self._process_dir(input_path, output_path)
    
    def _process_link(self, link_path: str) -> str:
        return LinkProcessor().get_link_path(link_path)

    def _process_file(self, input_file_path: str, output_file_path: str) -> None:
        if self.parse_args.encrypt:
            encrypt_file(input_file_path, output_file_path, PasswordHandler().get_password())
        elif self.parse_args.decrypt:
            decrypt_file(input_file_path, output_file_path, PasswordHandler().get_password())

    def _process_dir(self, input_dir: str, output_dir: str) -> None:
        for root, _, files in os.walk(input_dir):
            relative_path: str = os.path.relpath(root, input_dir)
            output_root: str = os.path.join(output_dir, relative_path)

            if not os.path.exists(output_root):
                os.makedirs(output_root)

            for file_name in files:
                input_file_path: str = os.path.join(root, file_name)
                output_file_path: str = os.path.join(output_root, file_name)
                self._process_path(input_file_path, output_file_path)
