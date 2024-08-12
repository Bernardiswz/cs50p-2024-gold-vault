"""
This module provides a factory for creating instances objects of the Parser class.

The ParserFactory class is designed to encapsulate the creation logic for 
Parser objects, allowing for easy extension or modification of the parser 
creation process if needed in the future.
"""

from ..parser import Parser


__all__ = ["ParserFactory"]


class ParserFactory:
    """
    A factory class for creating Parser instances.

    The ParserFactory class provides a static method for creating
    instances of the Parser class. This design pattern allows for
    the creation logic to be centralized and easily modified if
    additional configuration or customization is required in the future.
    """

    @staticmethod
    def create_parser() -> Parser:
        """
        Creates and returns a new instance of the Parser class.

        This static method instantiates a Parser object and returns it.

        Returns:
            Parser: A new instance of the Parser class.
        """
        return Parser()
