"""
Contains the class and package interfaces to the functionality related to error handling.

Packages:
- exceptions: Contain modules with custom exceptions for the parser and crypto packages.
- messages: 
    Contain constants of messages to be displayed as output or feedback from errors and related functionality. For the
    crypto and parser packages.
- type: This package contain the type of ErrorHandler to be used on type hinting and checking.

Classes:
- ErrorHandler: The class that contains the logic for ErrorHandling and related functionality.
- ErrorHandlerFactory: 
    This factory classes abstract the creation of ErrorHandler objects, providing an interface for this behavior.

"""

from .error_handler import ErrorHandler
from . import exceptions, messages, type
from .factory.error_handler_factory import ErrorHandlerFactory


__all__ = ["ErrorHandler", "exceptions", "messages", "type", "ErrorHandlerFactory"]
