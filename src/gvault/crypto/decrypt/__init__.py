"""
Contains the functions to perform decryption of files and related processes.

Functions:
- decrypt_file: Attempts to decrypt 'input_path' and write it to its 'output_path' using 'password'.
- get_ciphertext: Extracts the plain encrypted data of a file's contents, skipping the bytes containing the salt and iv.
- get_salt_iv: 
    Extracts salt and iv from given encrypted data by retrieving respectively data on indexes [:16] and [16:32] from the
    encrypted data.
"""

from .decrypt import decrypt_file, get_ciphertext, get_salt_iv


__all__ = ["decrypt_file", "get_ciphertext", "get_salt_iv"]
