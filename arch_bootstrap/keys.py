# arch_bootstrap/keys.py
"""
Handle SSH and GPG key import and validation.
"""

import os
from pathlib import Path
from .utils import run, log
from . import config


def import_ssh_keys():
    """Import SSH public keys from the configured GitHub user."""
    github_user = config.get_github_user()
    ssh_dir = config.get_home_dir() / ".ssh"
    authorized_keys = ssh_dir / "authorized_keys"

    ssh_dir.mkdir(parents=True, exist_ok=True)

    try:
        log(f"Fetching SSH keys for GitHub user: {github_user}")
        run(["curl", "-s", f"https://github.com/{github_user}.keys", "-o", str(authorized_keys)])
        log(f"Keys saved to {authorized_keys}")
        return authorized_keys
    except Exception as e:
        log(f"Failed to import SSH keys: {e}")
        return None

