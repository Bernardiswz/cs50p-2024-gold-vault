"""
This module declares the structure of command line args to be passed

Contains Parser class and interface for creating the parser in its specified
structure.
"""

import argparse


__all__ = ["Parser"]


class Parser:
    """
    Contain methods to build the expected structure and usage of command line args, and provides interface method to
    retrieve them.
    """

    def __init__(self) -> None:
        """
        Create the parser, add mutually exclusive group of encryption and decryption, and call on _add_arguments.
        """
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(
            usage="gvault (-e | --encrypt | -d | --decrypt) input -o OUTPUT",
            description="Reversibly encrypt|decrypt input files to output files. Password prompted by user input for \
            encryption/decryption.",
        )
        # Group to store mutually exclusive encrypt/decrypt flags
        self.enc_dec_group: argparse._MutuallyExclusiveGroup = self.parser.add_mutually_exclusive_group(required=True)
        self._add_arguments()

    def parse_args(self) -> argparse.Namespace:
        """
        Parse the command line arguments given to the script according to the declared structure.

        Returns:
            argparse.Namespace.
        """
        return self.parser.parse_args()

    def _add_arguments(self) -> None:
        """
        Adds encryption and decryption flags, input arguments and output arguments flag.
        """
        self._add_enc_dec_flags()
        self._add_input_arg()
        self._add_output_arg_flag()

    def _add_enc_dec_flags(self) -> None:
        """
        Add encryption and decryption flags to mutually exclusive group (encrypt|decrypt).
        """
        self._add_encrypt_flag()
        self._add_decrypt_flag()

    def _add_input_arg(self) -> None:
        """
        Add argument of 'input_paths' to parser.
        """
        self.parser.add_argument("input_paths", help="Input file/directory paths to processing.", nargs="+", type=str)

    def _add_output_arg_flag(self) -> None:
        """
        Add argument of 'output_paths' to parser.
        """
        self.parser.add_argument(
            "-o",
            "--output_paths",
            nargs="+",
            help="Output file/directory paths post processing.",
            required=True,
            type=str,
        )

    def _add_encrypt_flag(self) -> None:
        """
        Add mutually exclusive -e|--encrypt flag to parser's mutually exclusive group.
        """
        self.enc_dec_group.add_argument("-e", "--encrypt", action="store_true", help="Toggle encryption usage.")

    def _add_decrypt_flag(self) -> None:
        """
        Add mutually exclusive -d|--decrypt flag to parser's mutually exclusive group.
        """
        self.enc_dec_group.add_argument("-d", "--decrypt", action="store_true", help="Toggle decryption usage.")
