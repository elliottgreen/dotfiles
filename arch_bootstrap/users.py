# arch_bootstrap/users.py
"""
Ensure the target user exists and has wheel privileges.
"""

import subprocess
from .utils import run, log
from . import config


def ensure_user():
    """Ensure target user exists."""
    user = config.get_user()

    try:
        res = subprocess.run(
            ["id", user],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if res.returncode == 0:
            log(f"User '{user}' already exists.")
            return

        log(f"Creating user '{user}'...")
        run(["useradd", "-m", "-G", "wheel", "-s", "/bin/bash", user])
        with open("/etc/sudoers", "a") as f:
            f.write("%wheel ALL=(ALL:ALL) NOPASSWD: ALL\n")
        log(f"User '{user}' created with wheel privileges.")
    except Exception as e:
        log(f"Error ensuring user: {e}")

