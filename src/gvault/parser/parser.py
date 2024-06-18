import re
import sys


class Parser:
    def __init__(self):
        self.start()

    def start(self):
        ...


class ParserStructure:
    parser_pattern: str = r"""
    ^\s*(-e|--encrypt|-d|--decrypt){1}\s+
    (-i|--input)?([^~)('!*<>:;,?\*|]+)\s+
    (-o|--output){1}\s+([^~)('!*<>:;,?\"*|]+)\s*"""

    PARSER_RE: re.Pattern = re.compile(parser_pattern, re.VERBOSE)
