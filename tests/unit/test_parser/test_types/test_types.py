from gvault.parser import parser_types  # type: ignore
from gvault.parser.error_handling import ErrorHandler  # type: ignore
from gvault.parser import Parser  # type: ignore
from gvault.parser import ParserValidator  # type: ignore


__all__ = ["TestTypes"]


class TestTypes:
    def test_error_handler_type(self) -> None:
        assert isinstance(ErrorHandler, parser_types.ErrorHandler)

    def test_parser_validator_type(self) -> None:
        assert isinstance(ParserValidator, parser_types.ParserValidator)

    def test_parser_type(self) -> None:
        assert isinstance(Parser, parser_types.Parser)
