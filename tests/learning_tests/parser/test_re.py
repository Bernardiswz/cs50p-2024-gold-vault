from re import Match
from typing import List, Tuple
from parser_re import PARSER_RE


test_cases: List[Tuple[str, bool]]= [
    ("-e file.py -o john.py", True),
    ("--encrypt app/file2.py -o app/file3.py", True),
    ("app.py -o app2.py", False),
    (" -e    app.py dir/app/new_app.bat  -o  app-3.json  OTHER_APP.jpeg  ", True)
]

def test_parser_pattern() -> None:
    for input_str, expected_result in test_cases:
        re_match: Match = PARSER_RE.match(input_str)
        assert (re_match is not None) == expected_result, f"Failed for input: {input_str}"


def test_matches_attributes() -> None:
    test_case_1: str = test_cases[0][0]
    case_1_match: Match = PARSER_RE.match(test_case_1)
    print_match_groups(case_1_match)
    assert case_1_match.group(1) == "-e", f"Failed for input: {case_1_match.group(1)}"


def print_match_groups(match_obj: Match) -> None:
    for group in match_obj.groups():
        print(group)


test_matches_attributes()
