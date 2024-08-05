import sys
from typing import Any
from .messages.parser_messages import USAGE


__all__ = ["ErrorHandler"]


class ErrorHandler:
    @staticmethod
    def handler_exit(message: str = "", code: int = 1) -> None:
        if message:
            print(message)
        sys.exit(code)

    def handle_exception(self, exception: Exception) -> None:
        pass

    def handle_parser_exception(self, parser_exception: Exception = None) -> None:
        message: str = ""
        if parser_exception:
            message: Any = getattr(parser_exception, "message")
        print(USAGE)
        self.handler_exit(message)

    def handle_crypto_exception(self, crypto_exception: Exception = None) -> None:
        message: str = ""
        if crypto_exception:
            message: Any = getattr(crypto_exception, "message")
        self.handler_exit(message)
