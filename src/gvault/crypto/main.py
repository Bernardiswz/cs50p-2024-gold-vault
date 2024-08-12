import argparse
from .crypto import Crypto
from gvault.error_handling import ErrorHandlerFactory  # type: ignore
from gvault.error_handling.type import ErrorHandler  # type: ignore
from gvault.error_handling.exceptions.crypto_exceptions import (  # type: ignore
    CyclicLinkError,
    DecryptionError,
    LinkRecursionDepthError,
)


def crypto_main(parse_args: argparse.Namespace) -> None:
    try:
        error_handler: ErrorHandler = ErrorHandlerFactory.create_handler()
        crypto: Crypto = Crypto(parse_args)
        crypto.process_paths()
    except (CyclicLinkError, DecryptionError, LinkRecursionDepthError) as e:
        error_handler.handle_crypto_exception(e)
    return None
