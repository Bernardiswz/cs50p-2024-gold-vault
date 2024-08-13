"""
Module contains LinkProcessor class to process and handle symlink file types that are given as input paths.
"""

import os
from gvault.error_handling.exceptions.crypto_exceptions import CyclicLinkError, LinkRecursionDepthError


__all__ = ["LinkProcessor"]


class LinkProcessor:
    """
    Contains methods and interface for processing symlinks and raises errors if any unexpected behavior
    is found.
    """

    def __init__(self, max_depth: int = 10) -> None:
        """
        Declare instance variables of '_visited_paths' (to keep track of the depth of links that point to other links)
        to be used on other methods aswell as declaring the 'max_depth' to state how deep the link can be processed to
        resolve its path.

        Args:
            max_depth (int).
        """
        self._visited_paths: set = set()
        self._max_depth: int = max_depth

    def get_link_path(self, link_path: str) -> str:
        """
        Returns the resolved path of a symlink through recursive approach and processing each link.

        If current 'link_path' islink, read and process it, if any unexpected behavior occurs, the processing
        methods will raise exceptions accordingly.

        Args:
            link_path (str): Path of the symlink file.

        Returns:
            (str): Resolved path of the symlink.
        """
        if os.path.islink(link_path):
            target_path: str = os.readlink(link_path)
            self._process_link_path(target_path)
            return self.get_link_path(target_path)
        else:
            return os.path.realpath(link_path)

    def _process_link_path(self, link_path: str) -> None:
        """
        Process the given 'link_path' by checking if it is in visited (cyclic link), add to visited (to later checks)
        and checks if the maximum depth of resolving the link has been reached.

        Args:
            link_path (str).
        """
        self._check_link_path_in_visited(link_path)
        self._add_path_to_visited(link_path)
        self._check_max_recursion_depth_reached(link_path)

    def _check_link_path_in_visited(self, link_path: str) -> None:
        """
        Checks whether the 'link_path' is in the '_visited_paths' instance variable of set. If it is, then it means
        it is a cyclic link.

        Args:
            link_path (str).

        Raises:
            CyclicLinkError.
        """
        if link_path in self._visited_paths:
            raise CyclicLinkError(link_path)

    def _add_path_to_visited(self, link_path: str) -> None:
        """
        Add 'link_path' to the '_visited_paths' set instance variable.

        Args:
            link_path (str).
        """
        self._visited_paths.add(link_path)

    def _check_max_recursion_depth_reached(self, link_path: str) -> None:
        """
        Check if the amount of elements in '_visited_paths' set instance variable reached the specified maximum depth to
        attempt to resolve a link. If so, raise LinkRecursionDepthError.

        Args:
            link_path (str).

        Raises:
            LinkRecursionDepthError.
        """
        if len(self._visited_paths) > self._max_depth:
            raise LinkRecursionDepthError(link_path)
