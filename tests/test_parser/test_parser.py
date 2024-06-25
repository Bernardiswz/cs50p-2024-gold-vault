import argparse
import pytest
from typing import Dict, List
from gvault.parser import Parser


@pytest.fixture
def parser_instance():
    return Parser()


@pytest.mark.parametrize("argv, expected", [
    (["script.py", "-e", "file.py", "-o", "output_file.py"], {"encrypt": True}),
    (["script.py", "--encrypt", "file.py", "-o", "output_file.py"], {"encrypt": True}),
])
def test_parse_args_encrypt_flag(parser_instance: Parser, 
                                 monkeypatch: pytest.MonkeyPatch, 
                                 argv: List[str], 
                                 expected: Dict[str, bool]):
    monkeypatch.setattr("sys.argv", argv)
    args: argparse.Namespace = parser_instance.parse_args()
    assert args.encrypt == expected["encrypt"]


def test_parse_args_decrypt_flag(parser_instance, monkeypatch):
    # Simulate command-line arguments
    monkeypatch.setattr("sys.argv", ["script.py", "-d", "input_file.txt", "-o", "output_file.txt"])

    # Parse arguments
    args = parser_instance.parse_args()

    # Assert expected behavior
    assert not args.encrypt  # Ensure encrypt flag is not set
    assert args.decrypt
    assert args.input == ["input_file.txt"]
    assert args.output == ["output_file.txt"]


def test_parse_args_missing_required(parser_instance, monkeypatch):
    # Simulate command-line arguments with missing required argument
    monkeypatch.setattr("sys.argv", ["script.py", "-e", "input_file.txt"])

    # Parse arguments and capture the error message (if any)
    with pytest.raises(SystemExit) as excinfo:
        parser_instance.parse_args()

    assert excinfo.type == SystemExit
    assert excinfo.value.code == 2  # Check for specific exit code (optional)
