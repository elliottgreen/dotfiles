# arch_bootstrap/repo.py
"""
Clone or update the dotfiles repository.
"""

from .utils import run, log
from . import config
from pathlib import Path


def ensure_repo():
    """Clone or update the dotfiles repository."""
    repo_dir = config.get_repo_dir()
    repo_url = config.get_repo_url()

    if not repo_dir.exists():
        log(f"Cloning repository from {repo_url}")
        run(["git", "clone", repo_url, str(repo_dir)])
    else:
        log("Repository already present, pulling latest changes.")
        run(["git", "-C", str(repo_dir), "pull"])

