import argparse
from typing import Union


from .error_handling.parser_exceptions import (
    PathsListLenError,
    PathNotFoundError,
    InvalidPathTypeError
)


from .factories import (
    ErrorHandlerFactory,
    ParserFactory, 
    ParserValidatorFactory,
)

from .parser_types import (
    ErrorHandler,
    Parser,
    ParserValidator
)


__all__ = ["get_parser"]


def get_parser() -> Union[argparse.Namespace, None]:
    parser: Parser = ParserFactory.create_parser()
    error_handler: ErrorHandler = ErrorHandlerFactory.create_handler()

    try:
        parse_args: argparse.Namespace = parser.parse_args()
        parser_validator: ParserValidator = ParserValidatorFactory.create_validator(parse_args)
        parser_validator.validate()
        return parse_args

    except PathsListLenError:
        error_handler.handle_paths_list_len_error()

    except PathNotFoundError as e:
        error_handler.handle_path_not_found(e.path)

    except InvalidPathTypeError as e:
        error_handler.handle_invalid_path_type(e.path)

    return None
