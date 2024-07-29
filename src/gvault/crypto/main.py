import argparse
from .crypto import Crypto
from .error_handling.error_handler import CryptoErrorHandler
from .error_handling.exceptions import CyclicLinkError, DecryptionError, LinkRecursionDepthError


def crypto_main(parse_args: argparse.Namespace) -> None:
    crypto: Crypto = Crypto(parse_args)
    error_handler: CryptoErrorHandler = CryptoErrorHandler()
    try:
        crypto.process_paths()
    except CyclicLinkError as e:
        error_handler.handle_cyclic_link(e)
    except DecryptionError as e:
        error_handler.handle_decryption_error(e)
    except LinkRecursionDepthError as e:
        error_handler.handle_link_recursion_depth_error(e)
    return None
