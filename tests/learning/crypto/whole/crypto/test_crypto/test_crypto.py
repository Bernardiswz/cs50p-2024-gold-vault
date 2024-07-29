import argparse
from gvault.crypto import crypto_main
from gvault.parser.get import get_parser


def main() -> None:
    parse_args: argparse.Namespace = get_parser()
    crypto_main(parse_args)


if __name__ == "__main__":
    main()
