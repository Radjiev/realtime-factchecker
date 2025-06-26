import importlib.util
from pathlib import Path

import pytest
from typer.testing import CliRunner

typer = pytest.importorskip("typer")

module_path = Path(__file__).resolve().parents[1] / "cli/factcheck.py"
spec = importlib.util.spec_from_file_location("cli_factcheck", module_path)
cli_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli_module)
app = cli_module.app


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
