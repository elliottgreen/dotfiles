import tempfile
import shutil
import pytest
from pathlib import Path
from .mocks import *

@pytest.fixture
def temp_home(tmp_path):
    """Temporary HOME directory for tests."""
    home = tmp_path / "home" / "testuser"
    home.mkdir(parents=True)
    return home

@pytest.fixture(autouse=True)
def patch_home(monkeypatch, fake_home):
    """Redirect HOME for all modules."""
    monkeypatch.setenv("HOME", str(fake_home))
    return fake_home

@pytest.fixture
def fake_pacman(monkeypatch, tmp_path):
    """Mock pacman command."""
    fake_bin = tmp_path / "fake_bin"
    fake_bin.mkdir()
    fake_pacman = fake_bin / "pacman"
    fake_pacman.write_text("#!/bin/sh\necho fake pacman \"$@\"\n")
    fake_pacman.chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake_bin}:{os.getenv('PATH')}")
    return fake_pacman

