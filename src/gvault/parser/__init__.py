"""
Contains the packages's entry points/interfaces of its subpackages/modules.

Packages:
- factories: Package containing factories of Parser and ParserValidator objects.
- parser_types: Package containing types/protocols to Parser and ParserValidator to usage on type hinting.

Classes:
- Parser: Class containing the app's parser declaration and interface to parse command line arguments.
- ParserValidator: Class containing the logic to perform validation on the arguments given on command line.

Functions:
- get_parser: 
    Entry point function to the whole package with all logic of parsing command line args, validating and returning the
    parse_args object.
"""

from .parser import Parser
from .parser_validator import ParserValidator
from .get import get_parser

from . import (
    factories,
    parser_types,
)


__all__ = ["factories", "Parser", "ParserValidator", "parser_types", "get_parser"]
