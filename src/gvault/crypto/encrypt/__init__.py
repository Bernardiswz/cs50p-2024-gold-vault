"""
This package contains functions related to encryption of files.

Functions:
- encrypt_file: 
    Reads data from input file given as its arg, then encrypts it and write to output path using a given password to
    make for a reversible decryption. Through key derivation with the password and usage of salt and iv.
- generate_salt_iv: Generate random bytes to be used as salt and iv.
"""

from .encrypt import encrypt_file, generate_salt_iv


__all__ = ["encrypt_file", "generate_salt_iv"]
