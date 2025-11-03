# tests/test_envdetect.py
import arch_bootstrap.envdetect as envdetect


def test_detect_env_wsl(monkeypatch):
    """Simulate WSL environment."""
    class FakeUname:
        release = "5.15.90.1-microsoft-standard-WSL2"

    monkeypatch.setattr(envdetect.platform, "uname", lambda: FakeUname())
    result = envdetect.detect_environment()
    assert result == "wsl"


def test_detect_env_fallback(monkeypatch, tmp_path):
    """Simulate a native environment."""
    # Remove /proc/1/cgroup and /.dockerenv if they exist
    monkeypatch.setattr(envdetect.os.path, "exists", lambda path: False)
    monkeypatch.setattr(envdetect.platform, "uname", lambda: type("U", (), {"release": "generic-linux"})())

    result = envdetect.detect_environment()
    assert result == "native"

