import re


__all__ = ["PARSER_RE"]

parser_pattern: str = r"""
^\s*(-e|--encrypt|-d|--decrypt){1}\s+
(-i|--input)?([^~)('!*<>:;,?\*|]+)\s+
(-o|--output){1}\s+([^~)('!*<>:;,?\"*|]+)\s*"""

PARSER_RE: re.Pattern = re.compile(parser_pattern, re.VERBOSE)
