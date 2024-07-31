import pytest
from unittest.mock import patch
from gvault.crypto.utils.link_processor import LinkProcessor # type: ignore
from gvault.crypto.error_handling.exceptions import CyclicLinkError, LinkRecursionDepthError # type: ignore


__all__ = ["TestLinkProcessor"]


class TestLinkProcessor:
    @pytest.fixture
    def link_processor(self) -> LinkProcessor:
        return LinkProcessor()

    def test_get_link_path_no_link(self, link_processor: LinkProcessor) -> None:
        with patch("os.path.islink", return_value=False), \
            patch("os.path.realpath", return_value="/path/to/real/file"):
            result = link_processor.get_link_path("/path/to/file")
            assert result == "/path/to/real/file"

    def test_get_link_path_simple_link(self, link_processor: LinkProcessor) -> None:
        with patch("os.path.islink", side_effect=[True, False]), \
            patch("os.readlink", return_value="/path/to/real/file"), \
            patch("os.path.realpath", return_value="/path/to/real/file"):
            result: str = link_processor.get_link_path("/path/to/link")
            assert result == "/path/to/real/file"

    def test_get_link_path_cyclic_link(self, link_processor: LinkProcessor) -> None:
        with patch("os.path.islink", side_effect=[True, True, True]), \
            patch("os.readlink", side_effect=["/path/to/link1", "/path/to/link2", "/path/to/link1"]):
            with pytest.raises(CyclicLinkError):
                link_processor.get_link_path("/path/to/link1")

    def test_get_link_path_max_depth_exceeded(self, link_processor: LinkProcessor) -> None:
        with patch("os.path.islink", return_value=True), \
            patch("os.readlink", return_value="/path/to/link"):
            for _ in range(link_processor._max_depth):
                link_processor._add_path_to_visited(f"/path/to/link{_}")
            with pytest.raises(LinkRecursionDepthError):
                link_processor.get_link_path("/path/to/link")
    
    def test_process_link_path_adds_to_visited(self, link_processor: LinkProcessor) -> None:
        link_path: str = "/path/to/link"
        link_processor._process_link_path(link_path)
        assert link_path in link_processor._visited_paths
    
    def test_check_link_path_in_visited_raises_error(self, link_processor: LinkProcessor) -> None:
        link_processor._visited_paths.add("/path/to/link")
        with pytest.raises(CyclicLinkError):
            link_processor._check_link_path_in_visited("/path/to/link")

    def test_check_max_recursion_depth_reached_raises_error(self, link_processor: LinkProcessor) -> None:
        for _ in range(link_processor._max_depth + 1): # Beyond max depth
            link_processor._visited_paths.add(f"/path/to/link{_}")
        with pytest.raises(LinkRecursionDepthError):
            link_processor._check_max_recursion_depth_reached("/path/to/link")
