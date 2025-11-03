#!/usr/bin/env python3
from arch_bootstrap.envdetect import detect_env
from arch_bootstrap.users import ensure_user
from arch_bootstrap.packages import ensure_packages
from arch_bootstrap.repo import ensure_repo
from arch_bootstrap.keys import import_ssh_keys, import_gpg_keys
from arch_bootstrap.dotfiles import apply_dotfiles
from arch_bootstrap.pam import configure_pam_u2f
from arch_bootstrap.utils import log, require_root

def main():
    require_root()
    env_type = detect_env()
    log(f"Detected environment: {env_type}")
    ensure_user()
    ensure_packages()
    ensure_repo()
    import_ssh_keys()
    import_gpg_keys()
    apply_dotfiles()
    configure_pam_u2f()
    log("Bootstrap complete!")

if __name__ == "__main__":
    main()

