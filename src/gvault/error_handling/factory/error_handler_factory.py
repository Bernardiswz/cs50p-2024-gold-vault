from ..error_handler.error_handler import ErrorHandler


__all__ = ["ErrorHandlerFactory"]


class ErrorHandlerFactory:
    @staticmethod
    def create_handler() -> ErrorHandler:
        return ErrorHandler()
