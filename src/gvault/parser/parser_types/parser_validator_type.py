from typing import List, Protocol, runtime_checkable

__all__ = ["ParserValidator"]


@runtime_checkable
class ParserValidator(Protocol):    
    def validate(self) -> None: # pragma: no cover
        ...

    def _validate_io_paths(self) -> None: # pragma: no cover
        ...

    def _validate_io_paths_list_len(self) -> None: # pragma: no cover
        ...
        
    def _validate_paths(self, paths_list: List[str]) -> None: # pragma: no cover
        ...
    
    def _validate_path_exists(self, path: str) -> None: # pragma: no cover
        ...

    def _validate_path_type(self, path: str) -> None: # pragma: no cover
        ...
