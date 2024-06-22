from ..parser import Parser


__all__ = ["ParserFactory"]


class ParserFactory:
    @staticmethod
    def create_parser() -> Parser:
        return Parser()
