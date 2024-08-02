import argparse
import pytest
from typing import List, Type
from gvault.parser import Parser  # type: ignore
from gvault.parser.parser_validator import ParserValidator  # type: ignore
from gvault.parser.factories import ParserFactory, ParserValidatorFactory  # type: ignore


__all__ = ["TestFactories"]


class TestFactories:
    PARSER_INSTANCE_ARGV: List[str] = ["script.py", "-e", "file.py", "-o", "output_file.py"]

    @pytest.fixture(autouse=True)
    def setup_method(self, parser: Parser, monkeypatch: pytest.MonkeyPatch) -> None:
        self.monkeypatch = monkeypatch
        self.parser_instance = parser
        self.parsed_args = self._parse_args()

    @pytest.fixture
    def parser(self) -> Parser:
        return Parser()

    def _parse_args(self) -> argparse.Namespace:
        self._set_monkeypatch_argv(self.PARSER_INSTANCE_ARGV)
        return self.parser_instance.parse_args()

    def _set_monkeypatch_argv(self, argv: List[str]) -> None:
        self.monkeypatch.setattr("sys.argv", argv)

    def test_parser_factory(self) -> None:
        parser: Parser = ParserFactory().create_parser()
        assert isinstance(parser, Parser)

    def test_validator_factory(self) -> None:
        validator: ParserValidator = ParserValidatorFactory().create_validator(self.parsed_args)
        assert isinstance(validator, ParserValidator)
