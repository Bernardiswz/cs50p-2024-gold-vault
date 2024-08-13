"""
This package contains all functionality related to the file IO operations, encryption and decryption of files and
processing of parsed args from the 'parser' package.

Packages:
- decrypt: All utility related to decrypting files (files that were encrypted by encrypt).
- encrypt: All utility related to encryption of files.
- utils: Helper and utility functions and classes to encrypt, decrypt and others.

Classes:
- Crypto: Interface class to perform the operations following the usage stated by 'parse_args'.

Functions:
- crypto_main: Entry point/interface of the package to process the 'parse_args' object (paths, encrypt, decrypt).
"""

from . import decrypt, encrypt, utils
from .crypto import Crypto
from .main import crypto_main


__all__ = ["decrypt", "encrypt", "utils", "Crypto", "crypto_main"]
