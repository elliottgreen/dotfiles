# tests/test_keys.py
from pathlib import Path
import arch_bootstrap.keys as keys


def test_import_ssh_keys(monkeypatch, tmp_path):
    """Verify SSH key import uses correct GitHub user and paths."""
    ssh_dir = tmp_path / ".ssh"
    ssh_dir.mkdir(parents=True)

    fake_keys_path = ssh_dir / "authorized_keys"

    # Mock config getters
    monkeypatch.setattr(keys.config, "get_home_dir", lambda: tmp_path)
    monkeypatch.setattr(keys.config, "get_github_user", lambda: "fakeuser")

    # Mock run() and log() to prevent real network calls
    called = {}

    def fake_run(cmd):
        called["cmd"] = cmd
        fake_keys_path.write_text("ssh-ed25519 AAAAB3NzaC1yc2EAAAADAQABAAABAQfakekey")

    monkeypatch.setattr(keys, "run", fake_run)
    monkeypatch.setattr(keys, "log", lambda msg: None)

    result = keys.import_ssh_keys()

    assert result == fake_keys_path
    assert fake_keys_path.exists()
    assert "fakeuser" in " ".join(called["cmd"])

