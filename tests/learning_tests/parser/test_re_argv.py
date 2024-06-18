"""
Test by passing correct/incorrect CLI args structure

Expected
[-e][--encrypt]|[-d][-decrypt]{1} [-i][--input]? [input_args]+ [-o]|[--output]{1} [output_args]+

"""
import re
import sys
from parser_re import PARSER_RE


def get_argv_str() -> str:
    # Exclude program's name
    return " ".join(sys.argv[1:])


def test_argv_re() -> None:
    re_match: re.Match = PARSER_RE.match(get_argv_str())
    return bool(re_match)


def main() -> None:
    print(get_argv_str())
    print(test_argv_re())

if __name__ == "__main__":
    main()
