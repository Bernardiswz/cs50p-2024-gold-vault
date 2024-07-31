import pytest
from gvault.crypto.error_handling.exceptions import ( # type: ignore
    CyclicLinkError, 
    DecryptionError, 
    LinkRecursionDepthError
)
from gvault.crypto.error_handling.error_messages import ( # type: ignore
    CYCLIC_LINK_ERROR, 
    DECRYPTION_ERROR, 
    LINK_RECURSION_DEPTH_ERROR
)


class TestExceptions:
    @pytest.mark.parametrize("link_path", ["link_path",])
    def test_cyclic_link_exception(self, link_path: str) -> None:
        with pytest.raises(CyclicLinkError) as excinfo:
            raise CyclicLinkError(link_path)
        exception_instance: CyclicLinkError = excinfo.value
        assert exception_instance.message == CYCLIC_LINK_ERROR.format(link_path)

    @pytest.mark.parametrize("file_path", ["some/path",])
    def test_decryption_error_exception(self, file_path: str) -> None:
        with pytest.raises(DecryptionError) as excinfo:
            raise DecryptionError(file_path)
        exception_instance: DecryptionError = excinfo.value
        assert exception_instance.message == DECRYPTION_ERROR.format(file_path)

    @pytest.mark.parametrize("link_path", ["link_path",])
    def test_link_recursion_depth_error(self, link_path: str) -> None:
        with pytest.raises(LinkRecursionDepthError) as excinfo:
            raise LinkRecursionDepthError(link_path)
        exception_instance: LinkRecursionDepthError = excinfo.value
        assert exception_instance.message == LINK_RECURSION_DEPTH_ERROR.format(link_path)
