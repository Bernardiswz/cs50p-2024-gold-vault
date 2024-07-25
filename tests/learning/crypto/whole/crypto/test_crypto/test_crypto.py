import argparse
from gvault.crypto.crypto import Crypto
from gvault.parser.get import get_parser


def main() -> None:
    parse_args: argparse.Namespace = get_parser()
    crypter: Crypto = Crypto(parse_args)
    crypter.process_paths()


if __name__ == "__main__":
    main()
