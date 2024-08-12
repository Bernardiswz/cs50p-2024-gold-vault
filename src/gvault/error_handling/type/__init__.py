"""
Act as package interface under the 'type' name of the package to prevent conflicts with the actual
ErrorHandler (type uses the same name for sake of simplicity).

Classes:
- ErrorHandler: The typing protocol to use on hinting following ErrorHandler structure.
"""

from .error_handler_type import ErrorHandler


__all__ = ["ErrorHandler"]
