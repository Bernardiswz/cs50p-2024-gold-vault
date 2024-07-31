from typing import Any, Callable
import pytest
from _pytest.capture import CaptureResult  # Type hinting
from gvault.crypto.error_handling.error_handler import CryptoErrorHandler # type: ignore
from gvault.crypto.error_handling.exceptions import ( # type: ignore
    CyclicLinkError,
    DecryptionError,
    LinkRecursionDepthError
)


__all__ = ["TestErrorHandler"]


class TestErrorHandler:
    @pytest.fixture
    def error_handler(self) -> CryptoErrorHandler:
        return CryptoErrorHandler()
    
    def _assert_err_message_in_outerr(self, capsys: pytest.CaptureFixture, error_message: str = "") -> None:
        captured: CaptureResult = capsys.readouterr()
        assert error_message in captured.out or error_message in captured.err

    def _assert_system_exit_with_message(
            self, 
            func: Callable[[Any],None], 
            capsys: pytest.CaptureFixture, 
            expected_message: str =None
            ) -> None:
        with pytest.raises(SystemExit) as excinfo:
            func()
        assert excinfo.type == SystemExit
        assert excinfo.value.code == 1
        if expected_message is not None:
            self._assert_err_message_in_outerr(capsys, expected_message)

    def test_crypto_exit(self, error_handler: CryptoErrorHandler, capsys: pytest.CaptureFixture) -> None:
        self._assert_system_exit_with_message(error_handler._crypto_exit, capsys)

    @pytest.mark.parametrize("link_path", ["/link_path",])
    def test_handle_cyclic_link(
        self,
        link_path: str, 
        error_handler: CryptoErrorHandler, 
        capsys: pytest.CaptureFixture
    ) -> None:
        cyclic_link_error: CyclicLinkError = CyclicLinkError(link_path)
        self._assert_system_exit_with_message(
            lambda: error_handler.handle_cyclic_link(cyclic_link_error),
            capsys,
            cyclic_link_error.message
        )

    @pytest.mark.parametrize("path", ["some/path",])
    def test_handle_decryption_error(
        self,
        path: str,
        error_handler: CryptoErrorHandler,
        capsys: pytest.CaptureFixture
    ) -> None:
        decryption_error: DecryptionError = DecryptionError(path)
        self._assert_system_exit_with_message(
            lambda: error_handler.handle_decryption_error(decryption_error),
            capsys,
            decryption_error.message
        )

    @pytest.mark.parametrize("path", ["some/path",])
    def test_handle_link_recursion_depth_error(
        self,
        path: str,
        error_handler: CryptoErrorHandler,
        capsys: pytest.CaptureFixture
    ) -> None:
        link_recursion_depth_error: LinkRecursionDepthError = LinkRecursionDepthError(path)
        self._assert_system_exit_with_message(
            lambda: error_handler.handle_link_recursion_depth_error(link_recursion_depth_error),
            capsys,
            link_recursion_depth_error.message
        )
