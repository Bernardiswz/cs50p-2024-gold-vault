from gvault.error_handling import ErrorHandlerFactory, ErrorHandler  # type: ignore


__all__ = ["TestFactory"]


class TestFactory:
    def test_factory(self) -> None:
        assert isinstance(ErrorHandlerFactory.create_handler(), ErrorHandler)
