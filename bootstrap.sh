#!/usr/bin/env bash
set -euo pipefail

# ============================================================
#  Arch Linux Bootstrap Script
#  - Supports multiple pkglist manifests
#  - Auto-detects environment (WSL / VM / Container / Bare metal)
#  - Configures SSH + GPG + secure sudo
# ============================================================

# ---- User settings ----
USER="drone"
GITHUB_USER="elliottgreen"
REPO_URL="https://github.com/${GITHUB_USER}/arch-setup.git"
REPO_DIR="/home/${USER}/arch-setup"

# ---- 0. Detect environment ----
detect_env() {
  if grep -qi microsoft /proc/version 2>/dev/null; then
    echo "wsl"
  elif [ -f /.dockerenv ]; then
    echo "container"
  elif systemd-detect-virt -vq; then
    echo "vm"
  else
    echo "baremetal"
  fi
}

ENV_TYPE=$(detect_env)
echo "[+] Detected environment: ${ENV_TYPE}"

# ---- 1. Base system packages ----
echo "[+] Installing base system packages..."
pacman -Syu --noconfirm git stow sudo base-devel curl gnupg openssh pam_ssh_agent_auth

# ---- 2. User setup ----
if ! id -u "$USER" &>/dev/null; then
  echo "[+] Creating user: $USER"
  useradd -m -G wheel -s /bin/bash "$USER"
  echo "%wheel ALL=(ALL:ALL) NOPASSWD: ALL" >>/etc/sudoers
fi

# ---- 3. Import SSH keys from GitHub ----
echo "[+] Importing SSH keys for $GITHUB_USER..."
sudo -u "$USER" bash <<EOF
mkdir -p ~/.ssh
curl -fsSL "https://github.com/${GITHUB_USER}.keys" -o ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
EOF

# ---- 4. Import GPG keys from GitHub ----
echo "[+] Importing GPG keys for $GITHUB_USER..."
sudo -u "$USER" bash <<EOF
mkdir -p ~/.gnupg
chmod 700 ~/.gnupg
curl -fsSL "https://github.com/${GITHUB_USER}.gpg" | gpg --import || true
EOF

# ---- 5. Clone dotfiles repo ----
sudo -u "$USER" bash <<EOF
if [ ! -d "$REPO_DIR" ]; then
    echo "[+] Cloning dotfiles repo..."
    git clone "$REPO_URL" "$REPO_DIR"
else
    echo "[+] Repo already present, pulling latest..."
    cd "$REPO_DIR" && git pull
fi

cd "$REPO_DIR"

# ---- 6. Install packages from manifests ----
echo "[+] Installing packages based on environment..."
PKGDIR="$REPO_DIR/package-lists"

if [ -d "$PKGDIR" ]; then
    # Always start with base, then environment-specific, then extra
    for list in "$PKGDIR/pkglist-base.txt" \
                "$PKGDIR/pkglist-${ENV_TYPE}.txt" \
                "$PKGDIR/pkglist-extra.txt"; do
        if [ -f "$list" ]; then
            echo "    -> Installing from $(basename "$list")"
            grep -vE '^#|^$' "$list" | xargs -r sudo pacman -S --needed --noconfirm
        fi
    done
else
    echo "[!] Warning: package-lists directory not found at $PKGDIR"
fi

# ---- 7. Apply dotfiles ----
echo "[+] Applying dotfiles..."
stow -t "\$HOME" -d "$REPO_DIR" dotfiles
EOF

# ---- 8. Remove NOPASSWD (hardening) ----
echo "[+] Hardening sudo configuration..."
sed -i '/NOPASSWD/d' /etc/sudoers
echo "%wheel ALL=(ALL:ALL) ALL" >>/etc/sudoers

# ---- 9. Enable SSH-agent-based sudo ----
echo "[+] Configuring pam_ssh_agent_auth..."
mkdir -p /etc/security/authorized_keys
cp /home/$USER/.ssh/authorized_keys /etc/security/authorized_keys/$USER
chown root:root /etc/security/authorized_keys/$USER
chmod 644 /etc/security/authorized_keys/$USER

if ! grep -q pam_ssh_agent_auth /etc/pam.d/sudo; then
  sed -i '1iauth sufficient pam_ssh_agent_auth.so file=/etc/security/authorized_keys/%u' /etc/pam.d/sudo
fi

echo "[✓] Bootstrap complete for environment: ${ENV_TYPE}"
