"""
This module contains a factory to generate validator objects to be used on the parser.

The ParserValidatorFactory encapsulates object creation logic of the parser validator,
and it can be easily extended as needed.
"""

import argparse
from ..parser_validator import ParserValidator


__all__ = ["ParserValidatorFactory"]


class ParserValidatorFactory:
    """
    A factory class for creating validator instances.

    This class contains a method similar in nature to that of parser factory.
    To create a validator object and return it given parse args.
    """

    @staticmethod
    def create_validator(parse_args: argparse.Namespace) -> ParserValidator:
        """
        Creates a ParserValidator objects with parameter of parse args and returns it.

        Args:
            parse_args (argparse.Namespace): Structure of the parsed command line arguments on the parser.
        Returns:
            ParserValidator object with parse_args parameter.
        """
        return ParserValidator(parse_args)
