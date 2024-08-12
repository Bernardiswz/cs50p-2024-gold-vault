"""
This package contains the type/protocols of Parser and ParserValidator classes for efficient type hinting.

Classes:
- Parser: Typing protocol of Parser class.
- ParserValidator: Typing protocol of ParserValidator.
"""

from .parser_type import Parser
from .parser_validator_type import ParserValidator


__all__ = ["Parser", "ParserValidator"]
