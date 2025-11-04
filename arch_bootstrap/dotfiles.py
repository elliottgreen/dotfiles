# arch_bootstrap/dotfiles.py
from .utils import run, log, command_exists
from . import config
from pathlib import Path


def apply_dotfiles():
    """
    Apply dotfiles via GNU Stow for the configured user.

    - Runs as the non-root user (via sudo -u)
    - Skips already-linked targets
    - Logs summary at the end
    """
    user = config.get_user()
    home_dir = config.get_home_dir()
    dotfiles_dir = config.get_dotfiles_dir()

    if not dotfiles_dir.exists():
        log("No dotfiles directory found — skipping.")
        return

    if not command_exists("stow"):
        log("Error: GNU Stow not found in PATH.")
        return

    log(f"Applying dotfiles from {dotfiles_dir} to {home_dir} as {user}...")

    applied = []
    skipped = []

    for subdir in sorted(dotfiles_dir.iterdir()):
        if not subdir.is_dir():
            continue  # skip non-directories like README.md

        target_link = home_dir / f".{subdir.name}"

        # check if already stowed (symlink exists or file already there)
        if target_link.exists() or target_link.is_symlink():
            skipped.append(subdir.name)
            continue

        try:
            run([
                "sudo", "-u", user, "stow",
                "-t", str(home_dir),
                "-d", str(dotfiles_dir),
                subdir.name
            ])
            applied.append(subdir.name)
        except Exception as e:
            log(f"Failed to stow {subdir.name}: {e}")

    # --- Summary ---
    if applied:
        log(f"✅ Applied dotfiles: {', '.join(applied)}")
    if skipped:
        log(f"⚙️  Skipped (already exists): {', '.join(skipped)}")
    if not applied and not skipped:
        log("No dotfiles found to apply.")

    log("Dotfile stow process complete.")

