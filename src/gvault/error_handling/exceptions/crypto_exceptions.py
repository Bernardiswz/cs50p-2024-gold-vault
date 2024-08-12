"""
Contains custom exceptions to be used on Crypto package.

CyclicLinkError, DecryptionError and LinkRecursionDepthError exceptions that inherit from base exception, 
with attributes of message and path that contains the path that caused the error. Properties and attributes
structured to be used in conjoint with the error handler (handle_crypto_exception).

Exception has message attribute declared from imported suiting error message, formated with the path
that caused the error.
"""

from ..messages.crypto_messages import CYCLIC_LINK_ERROR, DECRYPTION_ERROR, LINK_RECURSION_DEPTH_ERROR


__all__ = ["CyclicLinkError", "DecryptionError", "LinkRecursionDepthError"]


class CyclicLinkError(Exception):
    """
    Raised when a symlink is cyclic (points to itself or causes a loop).
    """

    def __init__(self, link_path: str) -> None:
        """
        Initializes base exception with instance variable message attribute and link_path.

        Args:
            link_path (str).
        """
        self.link_path: str = link_path
        self.message: str = CYCLIC_LINK_ERROR.format(self.link_path)
        super().__init__(self.message)


class DecryptionError(Exception):
    """
    Raised when decryption of file fails (unmatching password or another error).
    """

    def __init__(self, path: str) -> None:
        """
        Initializes base exception with instance variable message attribute and path.

        Args:
            path (str).
        """
        self.path: str = path
        self.message: str = DECRYPTION_ERROR.format(self.path)
        super().__init__(self.message)


class LinkRecursionDepthError(Exception):
    """
    Raised when specified recursion depth to resolve link path is reached.
    """

    def __init__(self, link_path: str) -> None:
        """
        Initializes base exception with instance variable message attribute and link_path.

        Args:
            link_path (str).
        """
        self.path: str = link_path
        self.message: str = LINK_RECURSION_DEPTH_ERROR.format(self.path)
        super().__init__(self.message)
