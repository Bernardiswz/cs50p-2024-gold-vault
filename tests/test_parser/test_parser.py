import argparse
import pytest
from typing import Dict, List
from gvault.parser import Parser


class TestParser:
    @pytest.fixture(autouse=True)
    def setup(self, parser_instance: Parser, monkeypatch: pytest.MonkeyPatch) -> None:
        self.parser_instance: Parser = parser_instance
        self.monkeypatch: pytest.MonkeyPatch = monkeypatch
    
    @pytest.fixture
    def parser_instance(self) -> Parser:
        return Parser()
    
    def set_monkeypatch_argv(self, argv: List[str]) -> None:
        self.monkeypatch.setattr("sys.argv", argv)
        
    def run_parse_args_test(self, argv: List[str]) -> None:
        self.set_monkeypatch_argv(argv)
        with pytest.raises(SystemExit) as excinfo:
            self.parser_instance.parse_args()
        assert excinfo.type == SystemExit
        assert excinfo.value.code == 2

    @pytest.mark.parametrize("argv, expected", [
        (["script.py", "-e", "file.py", "-o", "output_file.py"], {"encrypt": True}),
        (["script.py", "--encrypt", "file.py", "-o", "output_file.py"], {"encrypt": True}),
    ])
    def test_parse_args_encrypt_flag(self, argv: List[str], expected: Dict[str, bool]):
        self.set_monkeypatch_argv(argv)
        args: argparse.Namespace = self.parser_instance.parse_args()
        assert args.encrypt == expected["encrypt"]

    @pytest.mark.parametrize("argv, expected", [
        (["script.py", "-d", "file.py", "-o", "output_file.py"], {"decrypt": True}),
        (["script.py", "--decrypt", "file.py", "-o", "output_file.py"], {"decrypt": True}),
    ])
    def test_parse_args_decrypt_flag(self, argv: List[str], expected: Dict[str, bool]):
        self.set_monkeypatch_argv(argv)
        args: argparse.Namespace = self.parser_instance.parse_args()
        assert args.decrypt == expected["decrypt"]

    @pytest.mark.parametrize("argv, expected", [
        (["script.py", "-e", "file.py", "-o", "output_file.py"], 
        {"input": ["file.py"], "output": ["output_file.py"]}),
        (["script.py", "-e", "file.py", "file_2.py", "-o", "output_file.py", "output_file_2.py"],
        {"input": ["file.py", "file_2.py"], "output": ["output_file.py", "output_file_2.py"]}),
    ])
    def test_expected_input_output_parser_attr(self, argv: List[str], expected: Dict[str, List[str]]):
        self.set_monkeypatch_argv(argv)
        args: argparse.Namespace = self.parser_instance.parse_args()

        assert args.input == expected["input"]
        assert args.output == expected["output"]

    @pytest.mark.parametrize("argv", [
        ["script.py", "input_file.txt", "-o", "output_file.txt"]
    ])
    def test_missing_usage_type_flag(self, argv: List[str]):
        self.run_parse_args_test(argv)

    @pytest.mark.parametrize("argv", [
        ["script.py", "-o", "output_file.txt"]
    ])
    def test_missing_input_args(self, argv: List[str]):
        self.run_parse_args_test(argv)

    @pytest.mark.parametrize("argv", [
        ["script.py", "-e", "input_file.txt"]
    ])
    def test_missing_output_flag(self, argv: List[str]):
        self.run_parse_args_test(argv)

    @pytest.mark.parametrize("argv", [
        ["script.py", "-e", "-d", "input_file.txt", "output_file.txt"],
        ["script.py", "--encrypt", "--decrypt", "input_file.txt", "output_file.txt"],
        ["script.py", "-e", "input_file.txt", "output_file.txt", "-p"],
    ])
    def test_invalid_usage_flags(self, argv: List[str]):
        self.run_parse_args_test(argv)
