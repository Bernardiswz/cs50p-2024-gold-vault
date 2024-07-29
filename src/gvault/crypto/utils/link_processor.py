import os
from ..error_handling.exceptions import CyclicLinkError, LinkRecursionDepthError


__all__ = ["LinkProcessor"]


class LinkProcessor:
    def __init__(self, max_depth: int = 10) -> None:
        self._visited_paths: set = set()
        self._max_depth: int = max_depth

    def get_link_path(self, link_path: str) -> str:
        if os.path.islink(link_path):
            target_path: str = os.readlink(link_path)
            self._process_link_path(target_path)
            return self.get_link_path(target_path)
        else:
            return os.path.realpath(link_path)

    def _process_link_path(self, link_path: str) -> None:
        self._check_link_path_in_visited(link_path)
        self._add_path_to_visited(link_path)
        self._check_max_recursion_depth_reached(link_path)

    def _check_link_path_in_visited(self, link_path: str) -> None:
        if link_path in self._visited_paths:
            raise CyclicLinkError(link_path)

    def _add_path_to_visited(self, link_path: str) -> None:
        self._visited_paths.add(link_path)
        
    def _check_max_recursion_depth_reached(self, link_path: str) -> None:
        if len(self._visited_paths) > self._max_depth:
            raise LinkRecursionDepthError(link_path)
