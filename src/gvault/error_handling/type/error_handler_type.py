"""
Contains the protocol class meant to use for type hinting of ErrorHandler objects.

Methods:
- handler_exit: Call sys.exit and prints message, if given a code, is used as exit code to sys.exit.
- handle_exception: Handle default exception 'TODO'.
- handle_parser_exception:
    Prints the message displaying the USAGE of the program (attributes such as encrypt, decrypt) and then calls on
    handler_exit with the specific message attribute of the parser exception given as its argument.
- handle_crypto_exception: Calls on sys.exit using the message attribute of the exception argument given to it.
"""

from typing import Protocol, runtime_checkable


__all__ = ["ErrorHandler"]


@runtime_checkable
class ErrorHandler(Protocol):
    # Static method intended
    def handler_exit(self, message: str = "", code: int = 1) -> None:  # pragma: no cover
        ...

    def handle_exception(self, exception: Exception) -> None:  # pragma: no cover
        ...

    def handle_parser_exception(self, parser_exception: Exception = None) -> None:  # pragma: no cover
        ...

    def handle_crypto_exception(self, crypto_exception: Exception = None) -> None:  # pragma: no cover
        ...
