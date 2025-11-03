# arch_bootstrap/packages.py
"""
Ensure base and manifest packages are installed.
"""

import subprocess
from .utils import run, log
from . import config


BASE_PACKAGES = ["base-devel", "git", "stow"]


def ensure_packages():
    """Install base packages and any missing ones from manifests."""
    log("Checking base packages...")
    missing = []
    for pkg in BASE_PACKAGES:
        res = subprocess.run(
            ["pacman", "-Qi", pkg],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if res.returncode != 0:
            missing.append(pkg)

    if missing:
        log(f"Installing base packages: {' '.join(missing)}")
        run(["pacman", "-Syu", "--noconfirm"] + missing)
    else:
        log("All base packages already installed.")

    # Then, process manifest files dynamically
    pkgdir = config.get_pkgdir()
    if pkgdir.exists():
        manifests = sorted(pkgdir.glob("pkglist*.txt"))
        for mfile in manifests:
            log(f"Processing {mfile.name}")
            pkgs = [
                line.strip()
                for line in mfile.read_text().splitlines()
                if line.strip() and not line.startswith("#")
            ]
            to_install = []
            for pkg in pkgs:
                res = subprocess.run(
                    ["pacman", "-Qi", pkg],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                if res.returncode != 0:
                    to_install.append(pkg)
            if to_install:
                log(f"Installing from {mfile.name}: {' '.join(to_install)}")
                run(["pacman", "-S", "--needed", "--noconfirm"] + to_install)
            else:
                log(f"All packages from {mfile.name} already present.")
    else:
        log("No package-lists directory found, skipping.")

