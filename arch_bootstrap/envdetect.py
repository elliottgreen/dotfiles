# arch_bootstrap/envdetect.py
"""
Detect the environment type (e.g., WSL, container, or bare metal).
"""

import os
import platform
from .utils import log


def detect_environment() -> str:
    """Return a string describing the running environment."""
    try:
        # Detect WSL specifically
        if "microsoft" in platform.uname().release.lower():
            log("Detected WSL environment.")
            return "wsl"

        # Detect containers (generic check)
        if os.path.exists("/.dockerenv"):
            log("Detected container environment.")
            return "container"

        # Detect virtualized environment
        with open("/proc/1/cgroup", "rt") as f:
            if "docker" in f.read():
                log("Detected Docker cgroup.")
                return "container"

    except Exception as e:
        log(f"Environment detection failed: {e}")

    log("Detected native Linux environment.")
    return "native"

