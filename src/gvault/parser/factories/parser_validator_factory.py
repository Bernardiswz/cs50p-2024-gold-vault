from typing import List
from ..parser_validator import ParserValidator


__all__ = ["ParserValidatorFactory"]


class ParserValidatorFactory:
    @staticmethod
    def create_validator(input_paths: List[str], output_paths: List[str]) -> ParserValidator:
        return ParserValidator(input_paths, output_paths)
