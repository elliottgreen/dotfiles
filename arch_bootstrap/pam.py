# arch_bootstrap/pam.py
"""
Optionally configure pam_u2f for YubiKey authentication.
"""

import shutil
from pathlib import Path
from .utils import run, log
from . import config
from .envdetect import detect_environment


def configure_pam_u2f():
    """Optionally set up pam_u2f (only if available and not WSL)."""
    env_type = detect_environment()
    if env_type == "wsl":
        log("Detected WSL, skipping pam_u2f setup.")
        return

    pam_lib = Path("/usr/lib/security/pam_u2f.so")
    if not pam_lib.exists():
        log("pam_u2f not installed, skipping setup.")
        return

    log("Configuring pam_u2f for sudo...")
    user = config.get_user()
    home_dir = config.get_home_dir()
    yubico_dir = Path("/etc/Yubico")
    user_cfg = home_dir / ".config" / "Yubico" / "u2f_keys"
    yubico_dir.mkdir(parents=True, exist_ok=True)

    if not user_cfg.exists():
        log("Running pamu2fcfg to register YubiKey (touch device when prompted).")
        run([
            "sudo", "-u", user, "bash", "-c",
            "mkdir -p ~/.config/Yubico && pamu2fcfg > ~/.config/Yubico/u2f_keys"
        ])

    shutil.copy2(user_cfg, yubico_dir / "u2f_keys")

    pam_sudo_path = Path("/etc/pam.d/sudo")
    if pam_sudo_path.exists():
        original = pam_sudo_path.read_text()
        pam_sudo_path.write_text(f"auth required pam_u2f.so cue\n{original}")
    else:
        pam_sudo_path.write_text("auth required pam_u2f.so cue\n")

    log("pam_u2f configuration completed.")

