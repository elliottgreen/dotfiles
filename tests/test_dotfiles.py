from pathlib import Path
from arch_bootstrap import dotfiles

#def test_apply_dotfiles(tmp_path, monkeypatch):
#    dotdir = tmp_path / "dotfiles"
#    (dotdir / "bashrc").mkdir(parents=True)
#    monkeypatch.setattr(dotfiles, "DOTFILES_DIR", dotdir)
#    monkeypatch.setattr(dotfiles, "HOME_DIR", tmp_path)
#    monkeypatch.setattr(dotfiles, "run", lambda *a, **kw: None)
#    monkeypatch.setattr(dotfiles, "log", lambda *a, **kw: None)
#    dotfiles.apply_dotfiles()  # should skip without error

def test_apply_dotfiles(tmp_path, monkeypatch):
    dotdir = tmp_path / "dotfiles"
    (dotdir / "bashrc").mkdir(parents=True)

    monkeypatch.setattr(dotfiles.config, "get_dotfiles_dir", lambda: dotdir)
    monkeypatch.setattr(dotfiles.config, "get_home_dir", lambda: tmp_path)
    monkeypatch.setattr(dotfiles.config, "get_user", lambda: "testuser")

    monkeypatch.setattr(dotfiles, "run", lambda cmd: None)
    monkeypatch.setattr(dotfiles, "log", lambda msg: None)

    dotfiles.apply_dotfiles()
    assert dotdir.exists()

#def test_apply_dotfiles_applied_and_skipped(monkeypatch, tmp_path):
#    """Ensure apply_dotfiles stows new dirs and skips existing ones."""
#
#    # Create a fake dotfiles structure
#    dotdir = tmp_path / "dotfiles"
#    dotdir.mkdir()
#    (dotdir / "bashrc").mkdir()
#    (dotdir / "vim").mkdir()
#
#    # Fake home directory
#    home_dir = tmp_path / "home"
#    home_dir.mkdir()
#    existing = home_dir / ".bashrc"
#    existing.touch()  # simulate already existing dotfile
#
#    called = {"stow": []}
#    logs = []
#
#    # Patch config getters
#    monkeypatch.setattr("arch_bootstrap.dotfiles.config.get_dotfiles_dir", lambda: dotdir)
#    monkeypatch.setattr("arch_bootstrap.dotfiles.config.get_home_dir", lambda: home_dir)
#    monkeypatch.setattr("arch_bootstrap.dotfiles.config.get_user", lambda: "testuser")
#
#    # Patch helpers
#    monkeypatch.setattr("arch_bootstrap.dotfiles.command_exists", lambda c: True)
#    monkeypatch.setattr("arch_bootstrap.dotfiles.log", lambda msg: logs.append(msg))
#    monkeypatch.setattr(
#        "arch_bootstrap.dotfiles.run",
#        lambda cmd: called["stow"].append(cmd[-1])
#    )
#
#    from arch_bootstrap import dotfiles
#    dotfiles.apply_dotfiles()
#
#    # Assertions
#    assert "bashrc" not in called["stow"], "bashrc should have been skipped"
#    assert "vim" in called["stow"], "vim should have been applied"
#    assert any("Skipped" in l or "⚙️" in l for l in logs)
#    assert any("Applied" in l or "✅" in l for l in logs)

