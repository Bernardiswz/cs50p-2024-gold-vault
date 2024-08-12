import argparse
from gvault.crypto import crypto_main
from gvault.parser import get_parser # type: ignore


def cli_main() -> None:
    try:
        parse_args: argparse.Namespace = get_parser()
        crypto_main(parse_args)
    except Exception:
        pass


if __name__ == "__main__":
    cli_main()
