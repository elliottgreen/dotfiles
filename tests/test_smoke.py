"""
Smoke test for the arch_bootstrap test environment.
Ensures that mocks, imports, and environment setup are working correctly
before other tests run.
"""

from pathlib import Path
import subprocess
import os
import pytest

pytestmark = pytest.mark.smoke

def test_basic_environment():
    """Verify pytest is running in the correct project environment."""
    # Ensure we are in the project root (has pyproject.toml)
    assert Path("pyproject.toml").exists(), "pyproject.toml missing in project root"

    # Confirm arch_bootstrap package is importable
    import arch_bootstrap
    assert hasattr(arch_bootstrap, "__file__")

def test_fake_home_dir(monkeypatch):
    """Ensure the global mock layer created a fake HOME directory."""
    home = os.getenv("HOME")
    assert home, "HOME not set"
    assert Path(home).exists(), f"Fake home dir not found: {home}"

def test_mock_subprocess(monkeypatch):
    """Ensure subprocess.run is mocked by the global mocks."""
    from arch_bootstrap import utils
    result = subprocess.run(["echo", "hello"], capture_output=True, text=True)
    assert hasattr(result, "returncode"), "Mock subprocess did not return result"
    assert result.returncode == 0, "Mock subprocess should return success"
    assert "ok" in result.stdout, "Mock subprocess stdout mismatch"

def test_mock_log_and_run(monkeypatch):
    """Ensure our global fake log and run functions are applied."""
    from arch_bootstrap import utils
    assert callable(utils.log), "utils.log not callable"
    assert callable(utils.run), "utils.run not callable"

def test_fake_dirs(monkeypatch):
    """Ensure dynamic config paths exist in the fake environment."""
    from arch_bootstrap import config

    paths = {
        "HOME_DIR": config.get_home_dir(),
        "DOTFILES_DIR": config.get_dotfiles_dir(),
    }

    for name, path in paths.items():
        assert path.exists(), f"{name} not mocked: {path}"

def test_config_paths(monkeypatch):
    from arch_bootstrap import config
    summary = config.debug_summary()
    for k, v in summary.items():
        assert v, f"{k} is empty or unset"
