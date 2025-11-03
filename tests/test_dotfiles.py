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

