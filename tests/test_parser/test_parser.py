import argparse
import pytest
from typing import Dict, List
from gvault.parser import Parser


@pytest.fixture
def parser_instance():
    return Parser()


def run_parse_args_test(
        parser_instance: Parser,
        monkeypatch: pytest.MonkeyPatch, 
        argv: List[str]):
    monkeypatch.setattr("sys.argv", argv)

    with pytest.raises(SystemExit) as excinfo:
        parser_instance.parse_args()
    
    assert excinfo.type == SystemExit
    assert excinfo.value.code == 2


@pytest.mark.parametrize("argv, expected", [
    (["script.py", "-e", "file.py", "-o", "output_file.py"], {"encrypt": True}),
    (["script.py", "--encrypt", "file.py", "-o", "output_file.py"], {"encrypt": True}),
])
def test_parse_args_encrypt_flag(
        parser_instance: Parser,
        monkeypatch: pytest.MonkeyPatch, 
        argv: List[str], 
        expected: Dict[str, bool]):

    monkeypatch.setattr("sys.argv", argv)
    args: argparse.Namespace = parser_instance.parse_args()
    assert args.encrypt == expected["encrypt"]


@pytest.mark.parametrize("argv, expected", [
    (["script.py", "-d", "file.py", "-o", "output_file.py"], {"decrypt": True}),
    (["script.py", "--decrypt", "file.py", "-o", "output_file.py"], {"decrypt": True}),
])
def test_parse_args_decrypt_flag(
        parser_instance: Parser, 
        monkeypatch: pytest.MonkeyPatch, 
        argv: List[str], 
        expected: Dict[str, bool]):
    monkeypatch.setattr("sys.argv", argv)
    args: argparse.Namespace = parser_instance.parse_args()
    assert args.decrypt == expected["decrypt"]


@pytest.mark.parametrize("argv, expected", [
    (["script.py", "-e", "file.py", "-o", "output_file.py"], 
    {"input": ["file.py"], "output": ["output_file.py"]}),
    (["script.py", "-e", "file.py", "file_2.py", "-o", "output_file.py", "output_file_2.py"],
    {"input": ["file.py", "file_2.py"], "output": ["output_file.py", "output_file_2.py"]}),
])
def test_expected_input_output_parser_attr(
        parser_instance: Parser,
        monkeypatch: pytest.MonkeyPatch,
        argv: List[str],
        expected: Dict[str, List[str]]):
    monkeypatch.setattr("sys.argv", argv)
    args: argparse.Namespace = parser_instance.parse_args()

    assert args.input == expected["input"]
    assert args.output == expected["output"]


@pytest.mark.parametrize("argv", [
    ["script.py", "input_file.txt", "-o", "output_file.txt"]
])
def test_missing_usage_type_flag(
        parser_instance: Parser, 
        monkeypatch: pytest.MonkeyPatch, 
        argv: List[str]):
    run_parse_args_test(parser_instance, monkeypatch, argv)


@pytest.mark.parametrize("argv", [
    ["script.py", "-o", "output_file.txt"]
])
def test_missing_input_args(
        parser_instance: Parser,
        monkeypatch: pytest.MonkeyPatch,
        argv: List[str]):
    run_parse_args_test(parser_instance, monkeypatch, argv)


@pytest.mark.parametrize("argv", [
    ["script.py", "-e", "input_file.txt"]
])
def test_missing_output_flag(
        parser_instance: Parser, 
        monkeypatch: pytest.MonkeyPatch, 
        argv: List[str]):
    run_parse_args_test(parser_instance, monkeypatch, argv)


@pytest.mark.parametrize("argv", [
    ["script.py", "-e", "-d", "input_file.txt", "output_file.txt"],
    ["script.py", "--encrypt", "--decrypt", "input_file.txt", "output_file.txt"],
    ["script.py", "-e", "input_file.txt", "output_file.txt", "-p"],
])
def test_invalid_usage_flags(
        parser_instance: Parser,
        monkeypatch: pytest.MonkeyPatch,
        argv: List[str]):
    run_parse_args_test(parser_instance, monkeypatch, argv)
