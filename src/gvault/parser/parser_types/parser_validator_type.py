from typing import List, Protocol

__all__ = ["ParserValidator"]


class ParserValidator(Protocol):    
    def validate(self) -> None:
        ...

    def _validate_io_paths(self) -> None:
        ...

    def _validate_io_paths_list_len(self) -> None:
        ...
        
    def _validate_paths(self, paths_list: List[str]) -> None:
        ...
    
    def _validate_path_exists(self, path: str) -> None:
        ...

    def _validate_path_type(self, path: str) -> None:
        ...
