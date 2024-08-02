import argparse
from .crypto import Crypto
from gvault.error_handling import ErrorHandlerFactory
from gvault.error_handling.type import ErrorHandler
from gvault.error_handling.exceptions.crypto_exceptions import CyclicLinkError, DecryptionError, LinkRecursionDepthError


def crypto_main(parse_args: argparse.Namespace) -> None:
    crypto: Crypto = Crypto(parse_args)
    error_handler: ErrorHandler = ErrorHandlerFactory.create_handler()
    try:
        crypto.process_paths()
    except CyclicLinkError as e:
        error_handler.handle_crypto_exception(e)
    except DecryptionError as e:
        error_handler.handle_crypto_exception(e)
    except LinkRecursionDepthError as e:
        error_handler.handle_crypto_exception(e)
    return None
