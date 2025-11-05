# Just a way to organize my dots.

### Dots so far:
- glow
- zshrc
- neovim

## Manual Method (For now)

Your plan makes perfect sense — you can do each of those steps manually without relying on the full Python framework or Makefile right now. Here’s exactly how to execute each step safely and effectively on Arch Linux:

---

### **1. Install packages from a file using xargs and pacman**

Assuming your package list is named `packages.txt` and has one package per line:

```bash
sudo pacman -Syu --needed --noconfirm $(grep -v '^#' packages.txt | xargs)
```

🟢 **Explanation**

* `grep -v '^#'` skips comments or blank lines.
* `xargs` turns each line into an argument for pacman.
* `--needed` skips already-installed packages.
* `--noconfirm` automates the process.

If you prefer a more readable variant:

```bash
xargs -a packages.txt sudo pacman -Syu --needed --noconfirm
```

---

### **2. Add a new user and grant sudo privileges**

Replace `<username>` with your preferred name:

```bash
sudo useradd -m -G wheel -s /bin/bash <username>
sudo passwd <username>
```

Then enable sudo for the `wheel` group:

```bash
echo "%wheel ALL=(ALL:ALL) NOPASSWD: ALL" | sudo tee -a /etc/sudoers
```

> ✅ This mirrors the behavior in the `users.py` script — user creation with wheel privileges and passwordless sudo.
> ✅ FIX THIS AFTER SETUP!!!!!!!!
---

### **3. Clone your dotfiles repo and apply with GNU Stow**

Run as the new user (or use `sudo -u <username>`):
> Note: This pulls just one directory (*maybe two...*)

1. Initialize a new Git repository in your desired directory: (we'll say 'dots')
   ```bash
   git init
   ```

2. Add the remote repository:
   ```bash
   git remote add origin <repository-url>
   ```

3. Enable sparse checkout:
   ```bash
   git config core.sparseCheckout true
   ```

4. Specify the directory you want to pull by adding its path to the sparse-checkout file:
   ```bash
   echo "path/to/your/directory/" >> .git/info/sparse-checkout
   ```

5. Fetch and pull the specified directory:
   ```bash
   git fetch origin
   git pull origin master
   ```

Then for that folder:

```bash
cd dots
stow -t ~/.config .
```

Then steps 4 $ 5 again for dots that have to be in the home folder:
```bash
cd dots-home
stow -t ~ .
```

