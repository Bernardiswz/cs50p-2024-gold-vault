import argparse
from typing import Any, Dict, Generator, Union
import pytest
from unittest.mock import patch, MagicMock
from gvault.parser.get import get_parser  # type: ignore
from gvault.parser.error_handling.parser_exceptions import (  # type: ignore
    InvalidPathTypeError,
    PathsListLenError,
    PathNotFoundError,
)


__all__ = ["TestGet"]


@pytest.fixture
def patches() -> Generator[Dict[str, Any], Any, None]:
    with patch("gvault.parser.factories.ParserFactory.create_parser") as mock_create_parser, patch(
        "gvault.parser.factories.ErrorHandlerFactory.create_handler"
    ) as mock_create_handler, patch(
        "gvault.parser.factories.ParserValidatorFactory.create_validator"
    ) as mock_create_validator:

        mock_parser: MagicMock = MagicMock(spec=argparse.ArgumentParser)
        mock_parse_args: MagicMock = MagicMock(spec=argparse.Namespace)
        mock_validator: MagicMock = MagicMock()
        mock_handler: MagicMock = MagicMock()

        mock_create_parser.return_value = mock_parser
        mock_create_handler.return_value = mock_handler
        mock_create_validator.return_value = mock_validator
        mock_parser.parse_args.return_value = mock_parse_args

        yield {
            "mock_create_parser": mock_create_parser,
            "mock_create_handler": mock_create_handler,
            "mock_create_validator": mock_create_validator,
            "mock_parser": mock_parser,
            "mock_parse_args": mock_parse_args,
            "mock_validator": mock_validator,
            "mock_handler": mock_handler,
        }


class TestGet:
    def test_get_parser_success(self, patches) -> None:
        result: Union[argparse.Namespace, None] = get_parser()
        patches["mock_parser"].parse_args.assert_called_once()
        patches["mock_create_validator"].assert_called_once_with(patches["mock_parse_args"])
        patches["mock_validator"].validate.assert_called_once()
        assert result == patches["mock_parse_args"]
        patches["mock_handler"].handle_invalid_path_type.assert_not_called()
        patches["mock_handler"].handle_paths_list_len_error.assert_not_called()
        patches["mock_handler"].handle_path_not_found.assert_not_called()

    def test_get_parser_paths_list_len_error(self, patches) -> None:
        paths_list_len_error: PathsListLenError = PathsListLenError()
        patches["mock_validator"].validate.side_effect = paths_list_len_error
        result: Union[argparse.Namespace, None] = get_parser()
        patches["mock_parser"].parse_args.assert_called_once()
        patches["mock_validator"].validate.assert_called_once()
        patches["mock_handler"].handle_paths_list_len_error.assert_called_once_with(paths_list_len_error)
        assert result is None

    def test_get_parser_path_not_found_error(self, patches) -> None:
        path_not_found_error: PathNotFoundError = PathNotFoundError(path="some/path")
        patches["mock_validator"].validate.side_effect = path_not_found_error
        result: Union[argparse.Namespace, None] = get_parser()
        patches["mock_parser"].parse_args.assert_called_once()
        patches["mock_validator"].validate.assert_called_once()
        patches["mock_handler"].handle_path_not_found.assert_called_once_with(path_not_found_error)
        assert result is None

    def test_get_parser_invalid_path_type_error(self, patches) -> None:
        invalid_path_type_error: InvalidPathTypeError = InvalidPathTypeError(path="some/path")
        patches["mock_validator"].validate.side_effect = invalid_path_type_error
        result: Union[argparse.Namespace, None] = get_parser()
        patches["mock_parser"].parse_args.assert_called_once()
        patches["mock_validator"].validate.assert_called_once()
        patches["mock_handler"].handle_invalid_path_type.assert_called_once_with(invalid_path_type_error)
        assert result is None
