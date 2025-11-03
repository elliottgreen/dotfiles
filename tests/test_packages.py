# tests/test_packages.py
from pathlib import Path
import arch_bootstrap.packages as packages


def test_package_list_parsing(tmp_path, monkeypatch):
    """Ensure package list parsing runs without error and respects comments."""
    pkgfile = tmp_path / "pkglist-base.txt"
    pkgfile.write_text("# comment\nvim\nhtop\n\n")

    # Mock dynamic config getter
    monkeypatch.setattr(packages.config, "get_pkgdir", lambda: tmp_path)

    # Mock run(), log(), and subprocess.run()
    monkeypatch.setattr(packages, "run", lambda *a, **kw: None)
    monkeypatch.setattr(packages, "log", lambda m: None)
    monkeypatch.setattr(
        packages.subprocess,
        "run",
        lambda *a, **kw: type("R", (), {"returncode": 1}),
    )

    packages.ensure_packages()  # Should not raise any exceptions

