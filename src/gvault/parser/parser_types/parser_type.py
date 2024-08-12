"""
This module stores the typing protocol of Parser objects to optmize type hinting.

The Parser protocol contains the expected structure of methods and return types
for static type checking.

Methods:
- parse_args: Should return an argparse.Namespace object.
- _add_arguments: Calls _add_enc_dec_flags, _add_input_arg and _add_output_arg_flag.
- _add_enc_dec_flags: Calls _add_encrypt_flag and _add_decrypt_flag.
- _add_input_arg: Adds an input argument to the parser.
- _add_output_arg_flag: Adds an flag output argument flag.
- _add_encrypt_flag: Adds an encryption flag to mutually exclusive encrypt and decrypt group.
- _add_decrypt_flag: Adds an decryption flag to mutually exclusive encrypt and decrypt group.
"""

import argparse
from typing import Protocol, runtime_checkable


__all__ = ["Parser"]


@runtime_checkable
class Parser(Protocol):
    def parse_args(self) -> argparse.Namespace:  # pragma: no cover
        ...

    def _add_arguments(self) -> None:  # pragma: no cover
        ...

    def _add_enc_dec_flags(self) -> None:  # pragma: no cover
        ...

    def _add_input_arg(self) -> None:  # pragma: no cover
        ...

    def _add_output_arg_flag(self) -> None:  # pragma: no cover
        ...

    def _add_encrypt_flag(self) -> None:  # pragma: no cover
        ...

    def _add_decrypt_flag(self) -> None:  # pragma: no cover
        ...
