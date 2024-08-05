import pytest
from _pytest.capture import CaptureResult
from typing import Any, Callable, List, Type


__all__ = ["raise_sys_exit_and_get_excinfo", "excinfo_expected", "error_message_in_outerr"]


def raise_sys_exit_and_get_excinfo(
    func: Callable[[Any], Any],
    *args: Any,
) -> pytest.ExceptionInfo:
    with pytest.raises(SystemExit) as excinfo:
        if args:
            func(*args)
        else:
            func()  # type: ignore
    return excinfo


def excinfo_expected(excinfo: pytest.ExceptionInfo, code: int = 1, type: Type = SystemExit) -> bool:
    return excinfo.type == type and excinfo.value.code == code


def error_message_in_outerr(capsys: pytest.CaptureFixture, *error_messages: str) -> bool:
    captured: CaptureResult = capsys.readouterr()
    return True if [message in captured.out or message in captured.err for message in error_messages] else False
