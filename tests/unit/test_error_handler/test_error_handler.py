import pytest
from .error_handler_utils import error_message_in_outerr, excinfo_expected, raise_sys_exit_and_get_excinfo
from gvault.error_handling import ErrorHandler  # type: ignore


__all__ = ["TestErrorHandler"]


class TestErrorHandler:
    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        self.error_handler: ErrorHandler = ErrorHandler()

    def test_default_handler_exit(self) -> None:
        excinfo: pytest.ExceptionInfo = raise_sys_exit_and_get_excinfo(self.error_handler.handler_exit)
        assert excinfo_expected(excinfo)

    @pytest.mark.parametrize("message, code", [("Something went wrong!", 100), ("Another error!", 303)])
    def test_handler_exit(self, message: str, code: int, capsys: pytest.CaptureFixture) -> None:
        excinfo: pytest.ExceptionInfo = raise_sys_exit_and_get_excinfo(self.error_handler.handler_exit, message, code)
        assert excinfo_expected(excinfo, code)
        assert error_message_in_outerr(capsys, message)
