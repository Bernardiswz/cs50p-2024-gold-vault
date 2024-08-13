"""
This module contains the Crypto class to perform the operations on the 'parse_args' retrieved from 'parser' package and
will perform the operations according to the structure and arguments given to 'parse_args'.
"""

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
    """
    This class contains methods to process and handle file IO operations of encryption and decryption following the
    structure of 'parse_args'. It uses of crypto package's sub modules to perform the necessary procedures.
    """

    def __init__(self, parse_args: argparse.Namespace) -> None:
        """
        Declare 'parse_args' and 'link_processor' instance variables to be used throughout the class's methods.

        Args:
            parse_args (argparse.Namespace): The structure that contains the parsed command line arguments to gvault.
        """
        self.parse_args: argparse.Namespace = parse_args
        self.link_processor: LinkProcessor = LinkProcessor()

    def process_paths(self) -> None:
        """
        Interface method to process the paths stored in 'parse_args' input and output paths attributes.

        Iterates over each input and output path simultaneously through use of zip object. The order of input paths
        and output paths is thought of as:

        input_paths: List[str] = ['file_1.txt', 'file_2.txt']
        output_paths: List[str] = ['output_file_1.txt', 'output_file_2.txt']

        In which the output file is implicitly taken as the according input path at same index. So input_paths[0] will
        have its contents processed to output_paths[0].

        The actual processing of each path is handled by the `_process_path` method.
        """
        for input_path, output_path in zip(self.parse_args.input_paths, self.parse_args.output_paths):
            self._process_path(input_path, output_path)

    def _process_path(self, input_path: str, output_path: str) -> None:
        """
        Process the input path according to its path type. If file exists asks for confirmation to overwrite, if
        overwriting is not accepted. Return.

        Path type will return an string matching the path type. Then the path type is processed and calls referent
        functions based on its type. If path type is link, call on '_get_link' to attempt to resolve its path then
        call on '_process_path' again with the resolved path. If no other type, return.

        Args:
            input_path (str).
            output_path (str).
        """
        input_path_type: str = self._get_path_type(input_path)
        if not self._should_write_output_path(output_path):
            return
        match input_path_type:
            case "file":
                self._process_file(input_path, output_path)
            case "directory":
                self._process_dir(input_path, output_path)
            case "symlink":
                resolved_path: str = self._get_link(input_path)
                self._process_path(resolved_path, output_path)
            case _:
                return

    def _get_path_type(self, path: str) -> str:
        """
        Returns a string specifying the path type of 'path' through use of module 'os' functions/methods.

        Args:
            path (str).

        Returns
            (str): Containing the path type casted into a string.
        """
        if os.path.isfile(path):
            return "file"
        elif os.path.islink(path):
            return "symlink"
        elif os.path.isdir(path):
            return "directory"
        else:
            return "unknown"

    def _should_write_output_path(self, path: str) -> bool:
        """
        Checks if given 'path' exists, if so prompt confirmation to overwrite it. If path doesn't exist or overwrite
        operation is confirmed, returns True, else false.

        Args:
            path (str).

        Returns:
            (bool).
        """
        if os.path.exists(path):
            return self._confirm_overwrite_path(path)
        return True

    def _confirm_overwrite_path(self, path: str) -> bool:
        """
        Wrapper method to call on 'confirm_overwrite_path'.

        Args:
            path (str).

        Returns:
            (bool).
        """
        return confirm_overwrite_path(path)

    def _get_link(self, link_path: str) -> str:
        """
        Calls on wrapper method '_get_link_path' to retrieve and process the path of a link file given as argument.

        Args:
            link_path (str).

        Returns:
            (str): Resolved link path.
        """
        return self._get_link_path(link_path)

    def _get_link_path(self, link_path: str) -> str:
        """
        Uses instance variable 'link_processor' interface method to resolve and process 'link_path' to ensure integrity
        of the program's flow and file IO.

        Args:
            link_path (str).

        Returns:
            (str): Resolved link path.
        """
        self.link_processor.get_link_path(link_path)

    def _process_file(self, input_file_path: str, output_file_path: str) -> None:
        """
        Process a file type input path. Checks for usage type in 'parse_args' (encrypt|decrypt) and calls on wrapper
        methods of '_encrypt_file' or '_decrypt_file' accordingly.

        Args:
            input_file_path (str).
            output_file_path (str).
        """
        if self.parse_args.encrypt:
            self._encrypt_file(input_file_path, output_file_path)
        elif self.parse_args.decrypt:
            self._decrypt_file(input_file_path, output_file_path)

    def _encrypt_file(self, input_file_path: str, output_file_path: str) -> None:
        """
        Wrapper method to call on 'encrypt_file' function, and calls on wrapper method '_get_password' to give the
        function the password parameter.

        Args:
            input_file_path (str).
            output_file_path (str).
        """
        encrypt_file(input_file_path, output_file_path, self._get_password())

    def _decrypt_file(self, input_file_path: str, output_file_path: str) -> None:
        """
        Wrapper method to call on 'decrypt_file' function, and calls on wrapper method '_get_password' to give the
        function the password parameter.

        Args:
            input_file_path (str).
            output_file_path (str).
        """
        decrypt_file(input_file_path, output_file_path, self._get_password())

    def _get_password(self) -> str:
        """
        Returns the input extracted from the function 'getpass' to safely parse password strings to be later processed
        on the encrypt and decrypt file functions/modules.

        Returns:
            (str): Password.
        """
        return getpass("Password:")

    def _process_dir(self, input_dir: str, output_dir: str) -> None:
        """
        Process the directory path type. Iterates over the root dir and files through os.walk and constructs a matching
        structure but writing to the output path. As in:

        dir = input_dir/inner_dir/file_1.txt
        _process_dir(dir, output_dir)

        # Result: output_dir/inner_dir/file_1.txt
        """
        for root, _, files in os.walk(input_dir):
            relative_path: str = os.path.relpath(root, input_dir)
            output_root: str = os.path.join(output_dir, relative_path)
            if not self._should_write_output_path(output_root):
                continue
            self._make_output_dir(output_root)
            self._process_dir_child_items(files, root, output_root)

    def _make_output_dir(self, path: str) -> None:
        """
        Create an directory to specified path. This method is used by the process dir to build the  matching
        structure to the output path specified.

        Args:
            path (str).
        """
        os.makedirs(path)

    def _process_dir_child_items(self, files: List[str], root: str, output_root: str) -> None:
        """
        Method used by '_process_dir' to process the files of the input dir or any other directory related.
        For every file, get its true input and output path through os.path.join and then call on '_process_path' to
        process it.

        Args:
            files (List[str]): Files of the directory to be processed.
            root (str): Root directory of the input paths.
            output_root (str): Root directory of the output path, the one which the directory's files will be written.
        """
        for file_name in files:
            input_file_path: str = os.path.join(root, file_name)
            output_file_path: str = os.path.join(output_root, file_name)
            self._process_path(input_file_path, output_file_path)
