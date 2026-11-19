"""
Functional and Integration Tests for Official OsdagBridge Application.
Executes real functionality of available official modules and systematically
verifies application behavior, CLI commands, utility functions, code registries,
and documented entry points.
"""
from io import StringIO
from pathlib import Path
import subprocess
import sys
import pytest


@pytest.mark.smoke
@pytest.mark.integration
def test_official_repository_and_source_structure(official_root, official_source):
    """Verifies official repository root and Python source tree structure."""
    assert official_root.is_dir()
    assert (official_source / "osdagbridge").is_dir()
    assert (official_source / "osdagbridge" / "cli").is_dir()
    assert (official_source / "osdagbridge" / "core").is_dir()
    assert (official_source / "osdagbridge" / "desktop").is_dir()


@pytest.mark.functional
@pytest.mark.integration
def test_official_cli_analyze_command_execution(official_source, monkeypatch):
    """Executes the official CLI analyze command function and verifies output."""
    monkeypatch.syspath_prepend(str(official_source))
    from osdagbridge.cli.commands import analyze_cmd

    old_stdout = sys.stdout
    sys.stdout = buffer = StringIO()
    try:
        analyze_cmd("sample_bridge_project.json")
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    assert "analyze" in output
    assert "sample_bridge_project.json" in output


@pytest.mark.functional
@pytest.mark.integration
def test_official_units_conversion_canonical_si(official_source, monkeypatch):
    """Executes official units conversion helper function."""
    monkeypatch.syspath_prepend(str(official_source))
    from osdagbridge.core.utils.units import to_si

    assert to_si(24.0, "m") == 24.0
    assert to_si(500.0, "kN") == 500.0
    assert to_si(0.0, "mm") == 0.0


@pytest.mark.functional
@pytest.mark.integration
def test_official_input_validation_stub(official_source, monkeypatch):
    """Executes official validate_project utility function."""
    monkeypatch.syspath_prepend(str(official_source))
    from osdagbridge.core.utils.validation import validate_project

    result = validate_project({"span": 24.0})
    assert result is True


@pytest.mark.functional
@pytest.mark.integration
def test_official_code_registry_retrieval(official_source, monkeypatch):
    """Verifies official design code registry lookup and error handling."""
    monkeypatch.syspath_prepend(str(official_source))
    from osdagbridge.core.utils.codes.registry import get_code

    irc6 = get_code("IRC:6-2017")
    assert irc6 is not None
    non_existent = get_code("UNKNOWN_CODE_999")
    assert non_existent is None


@pytest.mark.functional
@pytest.mark.integration
def test_official_custom_exceptions_hierarchy(official_source, monkeypatch):
    """Verifies official domain exceptions inherit correctly from Exception."""
    monkeypatch.syspath_prepend(str(official_source))
    from osdagbridge.core.exceptions import OsdagError

    assert issubclass(OsdagError, Exception)
    with pytest.raises(OsdagError):
        raise OsdagError("Test structural exception")


@pytest.mark.functional
@pytest.mark.integration
def test_official_desktop_main_start(official_source, monkeypatch):
    """Verifies official desktop entry point executes its console stub."""
    monkeypatch.syspath_prepend(str(official_source))
    from osdagbridge.desktop.main import start

    old_stdout = sys.stdout
    sys.stdout = buffer = StringIO()
    try:
        start()
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    assert "Starting desktop UI" in output


@pytest.mark.regression
@pytest.mark.integration
def test_official_desktop_missing_main_module_execution(official_source):
    """
    Verifies OB-BUG-001: python -m osdagbridge.desktop fails with
    'No module named osdagbridge.desktop.__main__'.
    Reproducible execution evidence for bug OB-BUG-001.
    """
    env = dict(sys.modules)
    res = subprocess.run(
        [sys.executable, "-m", "osdagbridge.desktop"],
        cwd=str(official_source),
        capture_output=True,
        text=True,
    )
    assert res.returncode != 0
    assert "No module named osdagbridge.desktop.__main__" in res.stderr
