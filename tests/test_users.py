import subprocess
from pathlib import Path
from arch_bootstrap import users
import pathlib


def test_ensure_user_existing(monkeypatch, tmp_path):
    """Simulate an existing user."""
    monkeypatch.setattr(users.config, "get_user", lambda: "testuser")
    monkeypatch.setattr(users, "log", lambda m: None)
    monkeypatch.setattr(users, "run", lambda cmd, **kw: None)

    # Mock subprocess.run to simulate user already exists
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **kw: type("R", (), {"returncode": 0}),
    )

    # Redirect /etc/sudoers.d to temp dir
    fake_sudoers_d = tmp_path / "etc" / "sudoers.d"
    fake_sudoers_d.mkdir(parents=True)

    # Patch users.Path to redirect /etc/sudoers.d only
    def fake_path(arg):
        if str(arg) == "/etc/sudoers.d":
            return fake_sudoers_d
        return pathlib.Path(arg)

    monkeypatch.setattr(users, "Path", fake_path)

    users.ensure_user()
    # Verify no exceptions, drop-in created
    assert (fake_sudoers_d / "99-wheel-nopasswd").exists()


def test_ensure_user_creation(monkeypatch, tmp_path):
    """Simulate creating a missing user."""
    import builtins

    fake_sudoers = tmp_path / "sudoers"
    fake_sudoers_d = tmp_path / "etc" / "sudoers.d"
    fake_sudoers_d.mkdir(parents=True)
    real_open = builtins.open  # capture before patching

    monkeypatch.setattr(users.config, "get_user", lambda: "newuser")
    monkeypatch.setattr(users, "log", lambda m: None)
    monkeypatch.setattr(users, "run", lambda cmd, **kw: None)

    # Simulate "id" command failure
    def fake_run(cmd, **kwargs):
        if cmd[0] == "id":
            return type("R", (), {"returncode": 1})
        return type("R", (), {"returncode": 0})

    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(builtins, "open", lambda *a, **kw: real_open(fake_sudoers, "a"))

    # Patch users.Path to redirect /etc/sudoers.d only
    def fake_path(arg):
        if str(arg) == "/etc/sudoers.d":
            return fake_sudoers_d
        return pathlib.Path(arg)

    monkeypatch.setattr(users, "Path", fake_path)

    users.ensure_user()

    # Verify sudoers drop-in file exists
    wheel_file = fake_sudoers_d / "99-wheel-nopasswd"
    assert wheel_file.exists()
    assert "%wheel" in wheel_file.read_text()


def test_ensure_user_sudoers_d(monkeypatch, tmp_path):
    """Verify /etc/sudoers.d drop-in file is created correctly."""
    fake_etc = tmp_path / "etc"
    fake_etc.mkdir()
    sudoers_d = fake_etc / "sudoers.d"
    wheel_file = sudoers_d / "99-wheel-nopasswd"

    monkeypatch.setattr(users.config, "get_user", lambda: "testuser")
    monkeypatch.setattr(users, "log", lambda m: None)
    monkeypatch.setattr(users, "run", lambda cmd, **kw: None)

    # Simulate user missing initially
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **kw: type("R", (), {"returncode": 1}),
    )

    # Patch users.Path to redirect /etc/sudoers.d only
    def fake_path(arg):
        if str(arg) == "/etc/sudoers.d":
            return sudoers_d
        return pathlib.Path(arg)

    monkeypatch.setattr(users, "Path", fake_path)

    users.ensure_user()

    # Assertions
    assert wheel_file.exists(), "Sudoers drop-in was not created"
    text = wheel_file.read_text()
    assert "%wheel" in text and "NOPASSWD" in text

