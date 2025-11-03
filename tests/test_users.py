# tests/test_users.py
import subprocess
from arch_bootstrap import users


def test_ensure_user_existing(monkeypatch):
    """Simulate an existing user."""
    monkeypatch.setattr(users.config, "get_user", lambda: "testuser")
    monkeypatch.setattr(users, "log", lambda m: None)
    monkeypatch.setattr(users, "run", lambda cmd: None)

    # Mock subprocess.run to simulate user already exists (returncode=0)
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **kw: type("R", (), {"returncode": 0}),
    )

    users.ensure_user()  # should log "already exists"

def test_ensure_user_creation(monkeypatch, tmp_path):
    """Simulate creating a missing user."""
    import builtins

    fake_sudoers = tmp_path / "sudoers"
    real_open = builtins.open  # capture before patching

    monkeypatch.setattr(users.config, "get_user", lambda: "newuser")
    monkeypatch.setattr(users, "log", lambda m: None)
    monkeypatch.setattr(users, "run", lambda cmd: None)

    # Simulate "id" command failure
    def fake_run(cmd, **kwargs):
        if cmd[0] == "id":
            return type("R", (), {"returncode": 1})
        return type("R", (), {"returncode": 0})

    monkeypatch.setattr(subprocess, "run", fake_run)

    # Patch builtins.open safely (use real_open inside lambda)
    monkeypatch.setattr(builtins, "open", lambda *a, **kw: real_open(fake_sudoers, "a"))

    users.ensure_user()

    assert fake_sudoers.exists()
    assert "wheel" in fake_sudoers.read_text()

