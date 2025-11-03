# tests/test_pam.py
from pathlib import Path
import arch_bootstrap.pam as pam


def test_configure_pam_u2f_skipped(monkeypatch):
    """Ensure pam_u2f setup skips safely under WSL."""
    monkeypatch.setattr(pam, "detect_environment", lambda: "wsl")
    monkeypatch.setattr(pam, "log", lambda m: None)
    pam.configure_pam_u2f()  # should exit early with no errors


def test_configure_pam_u2f_missing_lib(monkeypatch, tmp_path):
    """Skip setup if pam_u2f.so not found."""
    monkeypatch.setattr(pam, "detect_environment", lambda: "native")
    monkeypatch.setattr(pam.Path, "exists", lambda self=None: False)
    monkeypatch.setattr(pam, "log", lambda m: None)
    pam.configure_pam_u2f()  # should skip without error

def test_configure_pam_u2f_success(monkeypatch, tmp_path):
    """Run through successful pam_u2f setup path without touching real /etc."""
    fake_user = "testuser"
    fake_home = tmp_path / "home" / fake_user
    fake_home.mkdir(parents=True)
    user_cfg = fake_home / ".config" / "Yubico" / "u2f_keys"
    user_cfg.parent.mkdir(parents=True)
    user_cfg.write_text("fakekey")

    fake_yubico = tmp_path / "etc" / "Yubico"
    fake_pam = tmp_path / "etc" / "pam.d"
    fake_pam.mkdir(parents=True)
    fake_pam_sudo = fake_pam / "sudo"
    fake_pam_sudo.write_text("")

    # Patch config and dependencies
    monkeypatch.setattr(pam, "detect_environment", lambda: "native")
    monkeypatch.setattr(pam.config, "get_user", lambda: fake_user)
    monkeypatch.setattr(pam.config, "get_home_dir", lambda: fake_home)
    monkeypatch.setattr(pam, "log", lambda m: None)
    monkeypatch.setattr(pam, "run", lambda *a, **kw: None)
    monkeypatch.setattr(pam.shutil, "copy2", lambda src, dst: None)

    # Save real Path methods before patching
    real_exists = pam.Path.exists
    real_write_text = pam.Path.write_text
    real_mkdir = pam.Path.mkdir

    def fake_exists(self):
        s = str(self)
        if s.endswith("pam_u2f.so") or s.endswith("u2f_keys"):
            return True
        return real_exists(self)

    def fake_write_text(self, text):
        s = str(self)
        if s.startswith("/etc/"):
            tmp_equiv = tmp_path / s.lstrip("/")
            tmp_equiv.parent.mkdir(parents=True, exist_ok=True)
            tmp_equiv.write_text(text)
            return
        return real_write_text(self, text)

    def fake_mkdir(self, *args, **kwargs):
        s = str(self)
        if s.startswith("/etc/"):
            tmp_equiv = tmp_path / s.lstrip("/")
            tmp_equiv.parent.mkdir(parents=True, exist_ok=True)
            return
        return real_mkdir(self, *args, **kwargs)

    monkeypatch.setattr(pam.Path, "exists", fake_exists)
    monkeypatch.setattr(pam.Path, "write_text", fake_write_text)
    monkeypatch.setattr(pam.Path, "mkdir", fake_mkdir)

    pam.configure_pam_u2f()  # should now complete without touching real /etc
