import argparse
from typing import Protocol


__all__ = ["Parser"]


class Parser(Protocol):
    def parse_args(self) -> argparse.Namespace:
        ...

    def _add_arguments(self) -> None:
        ...

    def _add_enc_dec_flags(self) -> None:
        ...

    def _add_input_arg(self) -> None:
        ...

    def _add_output_arg_flag(self) -> None:
        ...

    def _add_encrypt_flag(self) -> None:
        ...

    def _add_decrypt_flag(self) -> None:
        ...
