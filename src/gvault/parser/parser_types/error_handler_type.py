from typing import Protocol, runtime_checkable


__all__ = ["ErrorHandler"]


@runtime_checkable
class ErrorHandler(Protocol):
    # Static method intended
    def _parser_exit(self, message: str = "") -> None: # pragma: no cover
        ...

    def handle_invalid_path_type(self, path: str) -> None: # pragma: no cover
        ...

    def handle_paths_list_len_error(self) -> None: # pragma: no cover
        ...

    def handle_path_not_found(self, path: str) -> None: # pragma: no cover
        ...
