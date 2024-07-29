import sys
from .exceptions import CyclicLinkError, DecryptionError, LinkRecursionDepthError


class CryptoErrorHandler:
    @staticmethod
    def _crypto_exit(message: str = "") -> None:
        if message:
            print(message)
        sys.exit(1)

    def handle_cyclic_link(self, cyclic_link_error: CyclicLinkError) -> None:
        self._crypto_exit(cyclic_link_error.message)

    def handle_decryption_error(self, decryption_error: DecryptionError) -> None:
        self._crypto_exit(decryption_error.message)

    def handle_link_recursion_depth_error(self, link_recursion_depth_error: LinkRecursionDepthError) -> None:
        self._crypto_exit(link_recursion_depth_error.message)
