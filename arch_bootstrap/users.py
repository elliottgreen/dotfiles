"""
Ensure the target user exists and has wheel privileges safely.
"""

import subprocess
from pathlib import Path
from .utils import run, log
from . import config


def ensure_user():
    """Ensure target user exists and has passwordless sudo privileges."""
    user = config.get_user()

    # --- Step 1: Check if user already exists ---
    res = subprocess.run(
        ["id", user],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if res.returncode == 0:
        log(f"User '{user}' already exists.")
    else:
        log(f"Creating user '{user}'...")
        run(["useradd", "-m", "-G", "wheel", "-s", "/bin/bash", user])
        log(f"User '{user}' created and added to 'wheel' group.")

    # --- Step 2: Ensure /etc/sudoers.d/wheel-nopasswd exists ---
    sudoers_d = Path("/etc/sudoers.d")
    sudoers_d.mkdir(parents=True, exist_ok=True)

    wheel_file = sudoers_d / "99-wheel-nopasswd"
    line = "%wheel ALL=(ALL:ALL) NOPASSWD: ALL\n"

    if wheel_file.exists():
        content = wheel_file.read_text()
        if line.strip() in content:
            log("Wheel sudoers drop-in already configured.")
        else:
            log("Appending wheel rule to existing sudoers drop-in.")
            with wheel_file.open("a") as f:
                f.write(line)
    else:
        log("Creating new sudoers drop-in for wheel group.")
        wheel_file.write_text(line)

    # --- Step 3: Lock permissions for security ---
    run(["chmod", "0440", str(wheel_file)])
    log("User privilege configuration complete.")

