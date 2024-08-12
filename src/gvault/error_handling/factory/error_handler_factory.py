"""
Contains ErrorHandlerFactory class to creation of ErrorHandler objects.
"""

from ..error_handler import ErrorHandler


__all__ = ["ErrorHandlerFactory"]


class ErrorHandlerFactory:
    """
    Contains static method that creates ErrorHandler obj.
    """

    @staticmethod
    def create_handler() -> ErrorHandler:
        """
        Returns:
            ErrorHandler, a plain instance of the ErrorHandler class.
        """
        return ErrorHandler()
