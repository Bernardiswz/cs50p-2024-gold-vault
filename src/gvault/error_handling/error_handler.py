"""
Contains the ErrorHandler class meant to handle errors that rise from Exceptions on packages parser and crypto.
"""

import sys
from typing import Any
from .messages.parser_messages import USAGE


__all__ = ["ErrorHandler"]


class ErrorHandler:
    """
    Contains static base error handling method that exits on error and outputs referent message. Other methods are added
    to fulfill further needs of more specific handling (as for crypto and parser packages).
    """

    @staticmethod
    def handler_exit(message: str = "", code: int = 1) -> None:
        """
        Static method prints message if any is given and exits with given exit code (if none given, 1).

        Args:
            message (str): Message to be outputted before calling sys.exit.
            code (int): Exit code to be given as argument to sys.exit.
        Raises:
            SystemExit.
        """
        if message:
            print(message)
        sys.exit(code)

    def handle_exception(self, exception: Exception) -> None:
        """
        Base method to handle default/generic/built-in exceptions, TODO

        Args:
            exception (Exception).
        """
        pass

    def handle_parser_exception(self, parser_exception: Exception = None) -> None:
        """
        Prints USAGE message from parser messages and calls handler exit giving parser_exception's message attr as arg.

        Attempts to get 'message' attribute from parser_exception and use it as arg to handler exit.

        Args:
            parser_exception (Exception): Custom exception class for parser errors.
        """
        message: str = ""
        if parser_exception:
            message: Any = getattr(parser_exception, "message")
        print(USAGE)
        self.handler_exit(message)

    def handle_crypto_exception(self, crypto_exception: Exception = None) -> None:
        """
        Calls handler_exit with message attribute from crypto_exception.

        Args:
            crypto_exception (Exception): Custom exception intended to use on the crypto package.
        """
        message: str = ""
        if crypto_exception:
            message: Any = getattr(crypto_exception, "message")
        self.handler_exit(message)
