# =============================================
# Arch Bootstrap Makefile
# =============================================

PYTHON ?= python3
MODULE := arch_bootstrap
MAIN := $(MODULE)/main.py

# Environment variables (can be overridden)
BOOTSTRAP_USER ?= $(shell whoami)
BOOTSTRAP_GITHUB_USER ?= $(BOOTSTRAP_USER)
BOOTSTRAP_REPO_URL ?= https://github.com/$(BOOTSTRAP_USER)/public-dots.git

# =============================================
# Default target
# =============================================

.DEFAULT_GOAL := help

# =============================================
# Main Targets
# =============================================

.PHONY: run
run: ## Run full Arch bootstrap process (user, packages, repo, dotfiles)
	@echo "==> Running Arch Bootstrap as $(BOOTSTRAP_USER)"
	sudo BOOTSTRAP_USER=$(BOOTSTRAP_USER) \
	     BOOTSTRAP_GITHUB_USER=$(BOOTSTRAP_GITHUB_USER) \
	     BOOTSTRAP_REPO_URL=$(BOOTSTRAP_REPO_URL) \
	     $(PYTHON) -m $(MODULE).main

.PHONY: test
test: ## Run full test suite
	@echo "==> Running all tests..."
	pytest -v tests

.PHONY: smoke
smoke: ## Run smoke tests only
	@echo "==> Running smoke tests..."
	pytest -m smoke -v

.PHONY: lint
lint: ## Run lint checks using ruff
	@echo "==> Running linter..."
	ruff check $(MODULE) tests

.PHONY: clean
clean: ## Remove build and cache artifacts
	@echo "==> Cleaning up..."
	rm -rf __pycache__ */__pycache__ .pytest_cache .ruff_cache *.egg-info build dist

.PHONY: env
env: ## Print current environment variable values
	@echo "BOOTSTRAP_USER        = $(BOOTSTRAP_USER)"
	@echo "BOOTSTRAP_GITHUB_USER = $(BOOTSTRAP_GITHUB_USER)"
	@echo "BOOTSTRAP_REPO_URL    = $(BOOTSTRAP_REPO_URL)"

.PHONY: setup-env
setup-env: ## Show example export commands
	@echo "export BOOTSTRAP_USER=$(BOOTSTRAP_USER)"
	@echo "export BOOTSTRAP_GITHUB_USER=$(BOOTSTRAP_GITHUB_USER)"
	@echo "export BOOTSTRAP_REPO_URL=$(BOOTSTRAP_REPO_URL)"

.PHONY: incus-run
incus-run: ## Run bootstrap inside an Incus container
	@echo "==> Running inside Incus container..."
	incus exec mycontainer -- $(PYTHON) -m $(MODULE).main

# =============================================
# Dynamic help (extracts ## comments)
# =============================================

.PHONY: help
help: ## Show this help message
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9\._-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""

