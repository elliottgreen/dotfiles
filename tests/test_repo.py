# tests/test_repo.py
from pathlib import Path
import arch_bootstrap.repo as repo


def test_repo_clone_and_update(tmp_path, monkeypatch):
    """Ensure cloning occurs when missing and pull occurs when exists."""
    fake_repo = tmp_path / "repo"
    fake_url = "https://github.com/fakeuser/public-dots.git"

    # Patch config and utils
    monkeypatch.setattr(repo.config, "get_repo_dir", lambda: fake_repo)
    monkeypatch.setattr(repo.config, "get_repo_url", lambda: fake_url)

    called = {"cmds": []}

    def fake_run(cmd):
        called["cmds"].append(cmd)

    monkeypatch.setattr(repo, "run", fake_run)
    monkeypatch.setattr(repo, "log", lambda *a, **kw: None)

    # First run → should clone
    repo.ensure_repo()
    assert any("clone" in c for cmd in called["cmds"] for c in cmd)

    # Create repo dir and run again → should pull
    fake_repo.mkdir()
    repo.ensure_repo()
    assert any("pull" in c for cmd in called["cmds"] for c in cmd)

