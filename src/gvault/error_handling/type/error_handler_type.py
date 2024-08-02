from typing import Protocol, runtime_checkable


__all__ = ["ErrorHandler"]


@runtime_checkable
class ErrorHandler(Protocol):
    # Static method intended
    def handler_exit(self, message: str = "", code: int = 1) -> None:  # pragma: no cover
        ...

    def handle_exception(self, exception: Exception) -> None: # pragma: no cover
        ...

    def handle_parser_exception(self, parser_exception: Exception = None) -> None: # pragma: no cover
        ...

    def handle_crypto_exception(self, crypto_exception: Exception = None) -> None: # pragma: no cover
        ...
