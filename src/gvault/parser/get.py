"""
Contains the interface/entry point to the parser module and related functionality.

Functions:
- get_parser: Entry point to parsing of command line args, validation and error handling.
"""

import argparse
from typing import Union
from .factories import (
    ParserFactory,
    ParserValidatorFactory,
)
from .parser_types import Parser, ParserValidator
from gvault.error_handling import ErrorHandlerFactory  # type: ignore
from gvault.error_handling.exceptions.parser_exceptions import (  # type: ignore
    PathsListLenError,
    PathNotFoundError,
    InvalidPathTypeError,
)
from gvault.error_handling.type import ErrorHandler  # type: ignore


__all__ = ["get_parser"]


def get_parser() -> Union[argparse.Namespace, None]:
    """
    Instantiate parser, process given command line arguments, validate, handle errors and return parse_args.

    Creates required objects of Parser, ErrorHandler and ParserValidator, then call on ParserValidator's validate
    method and catch any raised exceptions from it and handles accordingly.

    Returns:
        argparse.Namespace (parse_args) | None (System Exit if any error).
    """
    parser: Parser = ParserFactory.create_parser()
    error_handler: ErrorHandler = ErrorHandlerFactory.create_handler()
    try:
        parse_args: argparse.Namespace = parser.parse_args()
        parser_validator: ParserValidator = ParserValidatorFactory.create_validator(parse_args)
        parser_validator.validate()
        return parse_args
    except (PathsListLenError, PathNotFoundError, InvalidPathTypeError) as e:
        error_handler.handle_parser_exception(e)
    return None
