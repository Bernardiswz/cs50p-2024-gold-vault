"""
Contains the error messages to be used as attributes of the crypto package exceptions classes. Also used
for printing and displaying output for user.
"""

__all__ = ["CYCLIC_LINK_ERROR", "DECRYPTION_ERROR", "LINK_RECURSION_DEPTH_ERROR"]


CYCLIC_LINK_ERROR: str = "Error: Cyclic link detected '{}'."
DECRYPTION_ERROR: str = "Error: Decryption failed for path '{}'."
LINK_RECURSION_DEPTH_ERROR: str = "Error: Maximum recursion depth reached for: '{}'."
