from ..error_handling import ErrorHandler


__all__ = ["ErrorHandlerFactory"]


class ErrorHandlerFactory:
    @staticmethod
    def create_handler() -> ErrorHandler:
        return ErrorHandler()
