from getpass import getpass


__all__ = ["PasswordHandler"]


class PasswordHandler:
    def __init__(self) -> None:
        self._password: str = None

    def get_password(self) -> str:
        if self._password is None:
            self._password: str = getpass("Enter your password: ")
        return self._password
