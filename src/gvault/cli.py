"""
Module containing the interface to the gvault package.
"""

import argparse
import sys
from gvault.crypto import crypto_main  # type: ignore
from gvault.parser import get_parser  # type: ignore


def cli_main() -> None:
    """
    Attempts to get command line arguments and perform operations according to parsed args through 'crypto_main'. If any
    unexpected exception throughout the usage of the program. Exit with the exception message.
    """
    try:
        parse_args: argparse.Namespace = get_parser()
        crypto_main(parse_args)
    except Exception as e:
        sys.exit(e)


if __name__ == "__main__":
    cli_main()
