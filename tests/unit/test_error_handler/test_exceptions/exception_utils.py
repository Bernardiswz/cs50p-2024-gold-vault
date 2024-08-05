from typing import Any, NamedTuple


__all__ = ["ExceptionData", "exception_attr_is_expected"]


class ExceptionData(NamedTuple):
    exception: Exception
    attr: str
    expected: Any


def exception_attr_is_expected(exception_data: ExceptionData) -> bool:
    exception: Exception = exception_data.exception
    attr: str = exception_data.attr
    expected: Any = exception_data.expected
    return getattr(exception, attr) == expected
