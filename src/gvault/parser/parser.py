import argparse


__all__ = ["Parser"]


class Parser:
    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(
            usage="gvault (-e | --encrypt | -d | --decrypt) input -o OUTPUT",
            description="Reversibly encrypt|decrypt input files to output files. Password prompted by user input for \
            encryption/decryption."
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
            help="Input file/directory paths to processing.",
            nargs="+",
            type=str
        )

    def _add_output_arg_flag(self) -> None:
        self.parser.add_argument(
            "-o", "--output",
            nargs="+",
            help="Output file/directory paths post processing.",
            required=True,
            type=str
        )

    def _add_encrypt_flag(self) -> None:
        self.enc_dec_group.add_argument(
            "-e", "--encrypt",
            action="store_true",
            help="Toggle encryption usage."
        )

    def _add_decrypt_flag(self) -> None:
        self.enc_dec_group.add_argument(
            "-d", "--decrypt",
            action="store_true",
            help="Toggle decryption usage."
        )
