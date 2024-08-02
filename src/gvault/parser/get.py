import argparse
from typing import Union
from .factories import (
    ParserFactory,
    ParserValidatorFactory,
)
from .parser_types import Parser, ParserValidator
from gvault.error_handling import ErrorHandlerFactory # type: ignore
from gvault.error_handling.exceptions.parser_exceptions import ( # type: ignore
    PathsListLenError, 
    PathNotFoundError, 
    InvalidPathTypeError
)
from gvault.error_handling.type import ErrorHandler # type: ignore


__all__ = ["get_parser"]


def get_parser() -> Union[argparse.Namespace, None]:
    parser: Parser = ParserFactory.create_parser()
    error_handler: ErrorHandler = ErrorHandlerFactory.create_handler()
    try:
        parse_args: argparse.Namespace = parser.parse_args()
        parser_validator: ParserValidator = ParserValidatorFactory.create_validator(parse_args)
        parser_validator.validate()
        return parse_args
    except PathsListLenError as e:
        error_handler.handle_parser_exception(e)
    except PathNotFoundError as e:
        error_handler.handle_parser_exception(e)
    except InvalidPathTypeError as e:
        error_handler.handle_parser_exception(e)
    return None
