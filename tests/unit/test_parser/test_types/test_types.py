from gvault.parser import parser_types  # type: ignore
from gvault.parser import Parser  # type: ignore
from gvault.parser import ParserValidator  # type: ignore


__all__ = ["TestTypes"]


class TestTypes:
    def test_parser_validator_type(self) -> None:
        assert isinstance(ParserValidator, parser_types.ParserValidator)

    def test_parser_type(self) -> None:
        assert isinstance(Parser, parser_types.Parser)
