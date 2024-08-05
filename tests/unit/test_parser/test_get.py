import argparse
from typing import Any, Generator, Union
import pytest
from unittest.mock import patch, MagicMock
from gvault.parser.get import get_parser  # type: ignore
from gvault.error_handling.exceptions.parser_exceptions import (  # type: ignore
    InvalidPathTypeError,
    PathsListLenError,
    PathNotFoundError,
)


class Mocks:
    def __init__(self) -> None:
        self.mock_parser: MagicMock = MagicMock(spec=argparse.ArgumentParser)
        self.mock_parse_args: MagicMock = MagicMock(spec=argparse.Namespace)
        self.mock_validator: MagicMock = MagicMock()
        self.mock_handler: MagicMock = MagicMock()

        self.mock_create_parser: MagicMock = patch("gvault.parser.factories.ParserFactory.create_parser").start()
        self.mock_create_handler: MagicMock = patch("gvault.error_handling.ErrorHandlerFactory.create_handler").start()
        self.mock_create_validator: MagicMock = patch(
            "gvault.parser.factories.ParserValidatorFactory.create_validator"
        ).start()

        self.mock_create_parser.return_value = self.mock_parser
        self.mock_create_handler.return_value = self.mock_handler
        self.mock_create_validator.return_value = self.mock_validator
        self.mock_parser.parse_args.return_value = self.mock_parse_args

    def stop_patches(self) -> None:
        patch.stopall()


@pytest.fixture
def patches() -> Generator[Mocks, Any, None]:
    mocks: Mocks = Mocks()
    yield mocks
    mocks.stop_patches()


class TestGet:
    def test_get_parser_success(self, patches: Mocks) -> None:
        result: Union[argparse.Namespace, None] = get_parser()
        patches.mock_parser.parse_args.assert_called_once()
        patches.mock_create_validator.assert_called_once_with(patches.mock_parse_args)
        patches.mock_validator.validate.assert_called_once()
        assert result == patches.mock_parse_args
        patches.mock_handler.handle_parser_exception.assert_not_called()

    def test_get_parser_paths_list_len_error(self, patches: Mocks) -> None:
        paths_list_len_error: PathsListLenError = PathsListLenError()
        patches.mock_validator.validate.side_effect = paths_list_len_error
        result: Union[argparse.Namespace, None] = get_parser()
        patches.mock_parser.parse_args.assert_called_once()
        patches.mock_validator.validate.assert_called_once()
        patches.mock_handler.handle_parser_exception.assert_called_once_with(paths_list_len_error)
        assert result is None

    def test_get_parser_path_not_found_error(self, patches: Mocks) -> None:
        path_not_found_error: PathNotFoundError = PathNotFoundError(path="some/path")
        patches.mock_validator.validate.side_effect = path_not_found_error
        result: Union[argparse.Namespace, None] = get_parser()
        patches.mock_parser.parse_args.assert_called_once()
        patches.mock_validator.validate.assert_called_once()
        patches.mock_handler.handle_parser_exception.assert_called_once_with(path_not_found_error)
        assert result is None

    def test_get_parser_invalid_path_type_error(self, patches: Mocks) -> None:
        invalid_path_type_error: InvalidPathTypeError = InvalidPathTypeError(path="some/path")
        patches.mock_validator.validate.side_effect = invalid_path_type_error
        result: Union[argparse.Namespace, None] = get_parser()
        patches.mock_parser.parse_args.assert_called_once()
        patches.mock_validator.validate.assert_called_once()
        patches.mock_handler.handle_parser_exception.assert_called_once_with(invalid_path_type_error)
        assert result is None
