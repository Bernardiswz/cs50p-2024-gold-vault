import argparse
import getpass
from gvault.parser import get_parser # type: ignore


def main() -> None:
    try:
        parse_args: argparse.Namespace = get_parser()
        password: str = getpass.getpass("Password: ")
    except Exception:
        pass


if __name__ == "__main__":
    main()
