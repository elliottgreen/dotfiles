# arch_bootstrap/dotfiles.py
from .utils import run, log
from . import config
from pathlib import Path

def apply_dotfiles():
    """Apply dotfiles via stow (only if not linked)."""
    user = config.get_user()
    home_dir = config.get_home_dir()
    dotfiles_dir = config.get_dotfiles_dir()

    if not dotfiles_dir.exists():
        log("No dotfiles directory found, skipping.")
        return

    log("Applying dotfiles using stow...")
    for subdir in dotfiles_dir.iterdir():
        if subdir.is_dir():
            # Check if the symlink already exists
            target_link = home_dir / subdir.name
            if target_link.exists() or target_link.is_symlink():
                log(f"Skipping {subdir.name} (already exists).")
                continue
            run([
                "sudo", "-u", user, "stow",
                "-t", str(home_dir),
                "-d", str(dotfiles_dir),
                subdir.name
            ])

