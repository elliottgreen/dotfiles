# arch_bootstrap/config.py
"""
Global configuration for the Arch Bootstrap project.

Holds environment variables, directory paths, and constants
used across all modules.
"""

from pathlib import Path
import os

# ---------- USER & REPO SETTINGS ----------
def get_user() -> str:
    return os.getenv("BOOTSTRAP_USER", "youruser")

def get_github_user() -> str:
    return os.getenv("BOOTSTRAP_GITHUB_USER", "yourgithubusername")

def get_home_dir() -> Path:
    # Always resolves current HOME dynamically
    return Path(os.getenv("HOME", f"/home/{get_user()}"))

# GitHub repository URL for dotfiles or config
def get_repo_dir() -> Path:
    return get_home_dir() / "public-dots"

# ---------- PATHS ----------
def get_pkgdir() -> Path:
    return get_repo_dir() / "package-lists"

def get_dotfiles_dir() -> Path:
    return get_repo_dir() / "dotfiles"

def get_repo_url() -> str:
    return f"public-dots"

# Optional: environment-specific or runtime constants can go here
#LOG_LEVEL = os.getenv("BOOTSTRAP_LOG_LEVEL", "INFO")

def debug_summary():
    """Return a summary of resolved dynamic config values."""
    return {
        "USER": get_user(),
        "GITHUB_USER": get_github_user(),
        "HOME_DIR": str(get_home_dir()),
        "REPO_DIR": str(get_repo_dir()),
        "PKGDIR": str(get_pkgdir()),
        "DOTFILES_DIR": str(get_dotfiles_dir()),
    }

