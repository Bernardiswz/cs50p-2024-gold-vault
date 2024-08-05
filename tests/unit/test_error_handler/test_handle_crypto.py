import pytest
from .error_handler_utils import error_message_in_outerr, excinfo_expected, raise_sys_exit_and_get_excinfo
from gvault.error_handling import ErrorHandlerFactory  # type: ignore
from gvault.error_handling.type import ErrorHandler  # type: ignore
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


__all__ = ["TestHandleCrypto"]


class TestHandleCrypto:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.error_handler: ErrorHandler = ErrorHandlerFactory.create_handler()

    @pytest.mark.parametrize(
        "crypto_exception_instance, message",
        [
            (CyclicLinkError("linkpath"), CYCLIC_LINK_ERROR.format("linkpath")),
            (DecryptionError("path"), DECRYPTION_ERROR.format("path")),
            (LinkRecursionDepthError("/some/linkpath"), LINK_RECURSION_DEPTH_ERROR.format("/some/linkpath")),
        ],
    )
    def test_handle_crypto_exception(
        self, crypto_exception_instance: Exception, message: str, capsys: pytest.CaptureFixture
    ) -> None:
        excinfo: pytest.ExceptionInfo = raise_sys_exit_and_get_excinfo(
            self.error_handler.handle_crypto_exception, crypto_exception_instance
        )
        assert excinfo_expected(excinfo)
        assert error_message_in_outerr(capsys, message)
