import argparse
import pytest
from typing import Any, Generator
from unittest.mock import patch, MagicMock
from gvault.crypto import Crypto, crypto_main
from gvault.error_handling import ErrorHandler
from gvault.error_handling.exceptions.crypto_exceptions import CyclicLinkError, DecryptionError, LinkRecursionDepthError


class Mocks:
    def __init__(self) -> None:
        self.mock_parse_args: MagicMock = MagicMock(spec=argparse.ArgumentParser.parse_args)
        self.mock_handler: MagicMock = MagicMock(spec=ErrorHandler)
        self.mock_crypto: MagicMock = MagicMock(spec=Crypto)
        self.mock_crypto_constructor: MagicMock = patch("gvault.crypto.Crypto")
        self.mock_create_handler: MagicMock = patch("gvault.error_handling.ErrorHandlerFactory.create_handler").start()
        self.mock_process_paths: MagicMock = patch("gvault.crypto.Crypto.process_paths").start()
        self.mock_create_handler.return_value = self.mock_handler

    def stop_patches(self) -> None:
        patch.stopall()


@pytest.fixture
def patches() -> Generator[Mocks, Any, None]:
    mocks: Mocks = Mocks()
    yield mocks
    mocks.stop_patches()


class TestCryptoMain:
    def test_crypto_main_success(self, patches: Mocks) -> None:
        crypto_main(patches.mock_parse_args)
        patches.mock_create_handler.assert_called_once()
        patches.mock_process_paths.assert_called_once()
        patches.mock_handler.handle_crypto_exception.assert_not_called()

    @pytest.mark.parametrize(
        "exception_instance",
        [CyclicLinkError("link_path"), DecryptionError("path"), LinkRecursionDepthError("link_path")],
    )
    def test_crypto_main_fail(self, patches: Mocks, exception_instance: Exception) -> None:
        patches.mock_process_paths.side_effect = [exception_instance]
        crypto_main(patches.mock_parse_args)
        patches.mock_handler.handle_crypto_exception.assert_called_once_with(exception_instance)
