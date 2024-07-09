import argparse
from ..parser_validator import ParserValidator


__all__ = ["ParserValidatorFactory"]


class ParserValidatorFactory:
    @staticmethod
    def create_validator(parse_args: argparse.Namespace) -> ParserValidator:
        return ParserValidator(parse_args)
