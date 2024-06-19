import argparse


class Parser:
    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="Process input files and generate an output file."
        )
        # Group to store mutually exclusive encrypt/decrypt flags
        self.enc_dec_group: argparse._MutuallyExclusiveGroup = self.parser.add_mutually_exclusive_group()
        self._add_arguments()

    def parse_args(self) -> argparse.Namespace:
        return self.parser.parse_args()

    def _add_arguments(self) -> None:
        self._add_enc_dec_flags()
        self._add_input_arg()
        self._add_output_arg_flag()

    def _add_enc_dec_flags(self) -> None:
        self._add_encrypt_flag()
        self._add_decrypt_flag()

    def _add_input_arg(self) -> None:
        self.parser.add_argument(
            "input",
            nargs="+",
            required=True
        )

    def _add_output_arg_flag(self) -> None:
        self.parser.add_argument(
            "-o", "--output",
            nargs="+",
            required=True
        )

    def _add_encrypt_flag(self) -> None:
        self.enc_dec_group.add_argument(
            "-e", "--encrypt",
            action="store_true",
            required=True
        )

    def _add_decrypt_flag(self) -> None:
        self.enc_dec_group.add_argument(
            "-d", "--decrypt",
            action="store_true",
            required=True
        )
