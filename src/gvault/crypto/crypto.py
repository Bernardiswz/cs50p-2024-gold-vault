import argparse
import os
from .encrypt import encrypt_file
from .decrypt import decrypt_file


class Crypto:
    def __init__(self, parse_args: argparse.Namespace) -> None:
        self.parse_args: argparse.Namespace = parse_args

    def crypto(self, password: str) -> None:
        if self.parse_args.encrypt:
            ...
        elif self.parse_args.decrypt:
            ...
    
    def _encrypt_files(self, password: str) -> None:
        for input_path, output_path in zip(self.parse_args.input_paths, self.parse_args.output_paths):
            if os.path.isfile(input_path) or os.path.islink(input_path):
                encrypt_file(input_path, output_path, password)
            elif os.path.isdir(input_path):
                ...
    

    def _process_dir(self, input_dir: str, output_dir: str, password: str) -> None:
        for root, _, files in os.walk(input_dir):
            relative_path: str = os.path.relpath(root, input_dir)
            output_root: str = os.path.join(output_dir, relative_path)

            if not os.path.exists(output_root):
                os.makedirs(output_root)

            # Process files
            for file_name in files:
                input_file_path: str = os.path.join(root, file_name)
                output_file_path: str = os.path.join(output_root, file_name)
                # process_file(input_file_path, output_file_path)

    def _process_file(self, input_file_path, output_file_path, password) -> None:
        ...
