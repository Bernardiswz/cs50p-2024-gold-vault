"""
This module will act as the package's functionality interface to be integrated with the 'parser' package interface.
Contains the 'crypto_main' function.
"""

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
    """
    Try to process the 'input_paths' and 'output_paths' of 'parse_args' through the use of the Crypto class interface,
    if any exceptions are raised, handled accordingly through the ErrorHandler.

    Args:
        parse_args (argparse.Namespace): Structure containing the parsed arguments data.
    """
    try:
        error_handler: ErrorHandler = ErrorHandlerFactory.create_handler()
        crypto: Crypto = Crypto(parse_args)
        crypto.process_paths()
    except (CyclicLinkError, DecryptionError, LinkRecursionDepthError) as e:
        error_handler.handle_crypto_exception(e)
    return None
