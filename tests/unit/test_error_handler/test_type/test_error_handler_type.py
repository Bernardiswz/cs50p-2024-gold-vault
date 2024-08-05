from gvault.error_handling import ErrorHandler, type  # type: ignore


__all__ = ["TestType"]


class TestType:
    def test_error_handler_type(self) -> None:
        assert isinstance(ErrorHandler, type.ErrorHandler)
