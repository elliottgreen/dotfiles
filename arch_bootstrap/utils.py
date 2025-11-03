# arch_bootstrap/utils.py
import os
import subprocess
import sys
import shutil


def log(msg: str):
    print(f"[bootstrap] {msg}")


def run(cmd, check=True, capture=False):
    """Run a subprocess command safely, optionally capturing output."""
    log(f"Running: {' '.join(cmd)}")

    if capture:
        result = subprocess.run(
            cmd,
            check=check,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    else:
        result = subprocess.run(cmd, check=check, text=True)
    return result


def command_exists(cmd):
    """Return True if command exists in PATH."""
    return shutil.which(cmd) is not None


def require_root():
    """Exit if the user is not root."""
    if hasattr(os, "geteuid") and os.geteuid() != 0:
        sys.exit("This script must be run as root.")

