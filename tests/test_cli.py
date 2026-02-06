import pytest
from unittest.mock import Mock, patch

from cli.main import Cli


class TestCli:
    """Tests for the Cli class."""

    def test_init_stores_args(self):
        """Test that __init__ stores the args."""
        mock_args = Mock()
        mock_args.input = "test.yaml"
        mock_args.verbose = False

        cli = Cli(mock_args)

        assert cli.args == mock_args

    def test_without_fileinput_raises_system_exit(self):
        """Test that run() raises SystemExit when input is not provided."""
        mock_args = Mock()
        mock_args.input = None
        mock_args.verbose = False

        cli = Cli(mock_args)

        with pytest.raises(SystemExit) as exc_info:
            cli.run()
        assert str(exc_info.value) == "Please specify --input (-i)"

    def test_invalid_fileinput_raises_system_exit(self):
        """Test that run() raises SystemExit when input is not provided."""
        mock_args = Mock()
        mock_args.input = "test.exe"
        mock_args.verbose = False

        cli = Cli(mock_args)

        with pytest.raises(SystemExit) as exc_info:
            cli.run()
        assert str(exc_info.value) == "Please specify --input (-i) .lang/ .yaml or .yml"

    def test_run_with_empty_yaml_file(self, capsys):
        """Test behavior when YAML file is empty."""
        mock_args = Mock()
        mock_args.input = "empty.yaml"
        mock_args.verbose = False

        cli = Cli(mock_args)

        with pytest.raises(ValueError) as exc_info:
            cli.run()
        assert str(exc_info.value) == "File is empty or not found"

    def test_run_with_malformed_yaml_raises_exception(self):
        """Test behavior when YAML file is malformed."""
        mock_args = Mock()
        mock_args.input = "malformed.yaml"
        mock_args.verbose = False

        cli = Cli(mock_args)

        with patch("common.HyLangFile"):
            with pytest.raises(ValueError) as exc_info:
                cli.run()

            assert str(exc_info.value) == "File contains no valid data"

    def test_run_with_yaml_parse_error(self):
        """Test with a realistic YAML error (if using PyYAML)."""
        import yaml

        mock_args = Mock()
        mock_args.input = "bad.yaml"
        mock_args.verbose = False

        cli = Cli(mock_args)

        with pytest.raises(yaml.YAMLError):
            cli.run()