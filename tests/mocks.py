"""
Reusable test mocks for arch_bootstrap tests.
These fixtures and helpers prevent real network, filesystem, or subprocess access.
"""

import types
from pathlib import Path
import pytest

# -----------------------------
# Mock subprocess
# -----------------------------
def fake_run(cmd, **kwargs):
    """Simulate successful command execution."""
    class Result:
        def __init__(self):
            self.returncode = 0
            self.stdout = "ok\n"
            self.stderr = ""
    # Optional debug: print(f"[mock subprocess] {cmd}")
    return Result()


def fake_system_call(*args, **kwargs):
    """Generic no-op system call (used for chown, etc.)"""
    return None


# -----------------------------
# Mock log/run functions
# -----------------------------
def fake_log(msg):
    print(f"[mock log] {msg}")


def fake_command_exists(cmd):
    """Pretend every command exists."""
    return True


# -----------------------------
# Global fake dirs for HOME / REPO
# -----------------------------
@pytest.fixture
def fake_home(tmp_path_factory):
    """Create a unique fake HOME directory for each test."""
    # Generate a unique path for this test
    base = tmp_path_factory.mktemp("fake_home")
    home = base / "home" / "testuser"
    ssh = home / ".ssh"
    dotfiles = home / "public-dots" / "dotfiles"
    pkglist = home / "public-dots" / "package-lists"

    for p in [home, ssh, dotfiles, pkglist]:
        p.mkdir(parents=True, exist_ok=True)

    return home

# -----------------------------
# Patch all modules that need it
# -----------------------------
@pytest.fixture(autouse=True)
def apply_global_mocks(monkeypatch, fake_home):
    """
    Automatically mock all dangerous operations in arch_bootstrap modules.
    Runs for every test automatically.
    """

    import arch_bootstrap.config as cfg
    monkeypatch.setattr(cfg, "HOME_DIR", fake_home, raising=False)
    monkeypatch.setattr(cfg, "REPO_DIR", fake_home / "public-dots", raising=False)
    monkeypatch.setattr(cfg, "PKGDIR", fake_home / "public-dots" / "package-lists", raising=False)
    monkeypatch.setattr(cfg, "DOTFILES_DIR", fake_home / "public-dots" / "dotfiles", raising=False)


# Subprocess safety blanket
    import subprocess
    monkeypatch.setattr(subprocess, "run", fake_run)
    
    # Disable os.chown / os.system / etc.
    import os
    monkeypatch.setattr(os, "system", fake_system_call)
    monkeypatch.setattr(os, "chown", fake_system_call)
    
    # Return value not used — fixture auto-applies
    return True

