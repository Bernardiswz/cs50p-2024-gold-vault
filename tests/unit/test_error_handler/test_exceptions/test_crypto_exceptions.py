import pytest
from .exception_utils import ExceptionData, exception_attr_is_expected
from gvault.error_handling.exceptions.crypto_exceptions import (  # type: ignore
    CyclicLinkError,
    DecryptionError,
    LinkRecursionDepthError,
)
from gvault.error_handling.messages.crypto_messages import (  # type: ignore
    CYCLIC_LINK_ERROR,
    DECRYPTION_ERROR,
    LINK_RECURSION_DEPTH_ERROR,
)


__all__ = ["TestCryptoExceptions"]


class TestCryptoExceptions:
    @pytest.mark.parametrize(
        "exception_data",
        [
            (ExceptionData(CyclicLinkError("linkpath"), "message", CYCLIC_LINK_ERROR.format("linkpath"))),
            (
                ExceptionData(
                    DecryptionError("path"),
                    "message",
                    DECRYPTION_ERROR.format("path"),
                )
            ),
            (ExceptionData(LinkRecursionDepthError("path"), "message", LINK_RECURSION_DEPTH_ERROR.format("path"))),
        ],
    )
    def test_exception_attr_is_expected(self, exception_data: ExceptionData) -> None:
        assert exception_attr_is_expected(exception_data)
