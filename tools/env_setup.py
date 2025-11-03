#!/usr/bin/env python3
"""
Interactive environment setup helper for Arch Bootstrap.
Lets you view and update environment variables such as
BOOTSTRAP_USER and BOOTSTRAP_GITHUB_USER.
"""

import os
import sys
from textwrap import dedent

# Environment variables managed by this tool
ENV_VARS = [
    ("BOOTSTRAP_USER", "Target system username"),
    ("BOOTSTRAP_GITHUB_USER", "GitHub username for cloning repos and SSH keys"),
]


def print_header():
    print("\n=== Arch Bootstrap Environment Setup ===")
    print("This tool manages environment variables used by bootstrap and pytest.\n")


def print_env():
    print("Current environment variable values:\n")
    for key, desc in ENV_VARS:
        value = os.getenv(key, "<unset>")
        print(f"  {key:<25} {value}")
        print(f"      {desc}")
    print("")


def choose_variable():
    print("Which variable do you want to change?")
    for i, (key, _) in enumerate(ENV_VARS, start=1):
        print(f"  {i}. {key}")
    print(f"  {len(ENV_VARS) + 1}. Exit")

    try:
        choice = int(input("\nEnter choice number: ").strip())
        if choice < 1 or choice > len(ENV_VARS) + 1:
            print("Invalid choice.\n")
            return None
        return choice
    except ValueError:
        print("Invalid input. Please enter a number.\n")
        return None


def update_variable(index):
    key, desc = ENV_VARS[index]
    current = os.getenv(key, "<unset>")
    print(f"\nCurrent value of {key}: {current}")
    new_value = input(f"Enter new value for {key} (or leave blank to cancel): ").strip()
    if not new_value:
        print("No change made.\n")
        return
    os.environ[key] = new_value
    print(f"{key} updated to '{new_value}'\n")

def save_to_env_file(env_file=".env"):
    """Write current environment variables to a .env file."""
    print(f"\nSaving environment to {env_file} ...")
    with open(env_file, "w") as f:
        for key, _ in ENV_VARS:
            value = os.getenv(key, "")
            f.write(f"{key}={value}\n")
    print(f"Environment saved to {env_file}.\n"
          f"You can load it automatically next time by running 'uv sync' or 'make'.")


def main():
    print_header()
    while True:
        print_env()
        choice = choose_variable()
        if choice is None:
            continue
        if choice == len(ENV_VARS) + 1:
            print("Exiting setup.\n")
            break
        update_variable(choice - 1)

    # Final summary
    print("Final environment configuration:\n")
    for key, _ in ENV_VARS:
        print(f"  {key:<25} {os.getenv(key)}")

    save = input("\nWould you like to save these to a .env file? [y/N]: ").strip().lower()
    if save == "y":
        save_to_env_file()
    print("Done.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)

