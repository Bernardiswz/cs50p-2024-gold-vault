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
