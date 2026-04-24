# 🛡️ VPS Image Tool

> A robust VPS backup system using SSH + `dd`.

---

## 🚀 Installation

To install the tool locally, navigate to the project directory and run:

```bash
pip install -e .
```

*This will install the tool in editable mode, allowing you to run the `vps-tool` command globally from your terminal.*

---

## ⚙️ Configuration

Before using the tool, you must configure your VPS IP address. You can easily do this by running the initialization command:

```bash
vps-tool init
```

To update your IP address later on, you can run:
```bash
vps-tool edit-ip
```

This will prompt you for your VPS IP and save it securely in a `.env` file!

*(Note: The `.env` file is ignored by Git, so your IP address won't be pushed to the repository.)*

---

## 📖 User Manual

### 💾 Where are images stored?
By default, running `vps-tool backup` will interactively prompt you for a save location, defaulting to `backup.img.gz` in your current working directory. You can also specify the path directly:
```bash
vps-tool backup /path/to/custom/folder/my-backup.img.gz
```
The command pipes the disk image over SSH and saves it directly to the specified file.

### 🔍 Inspecting Images
When you run `vps-tool inspect <image>`, the image is mounted to `/tmp/vps_mount` (or the `DEFAULT_MOUNT` set in `config.py`). You can browse its files there until you press `ENTER` to unmount it.

### 📁 Folder Purposes
The repository includes several directories meant to help organize your workflow:

| Directory | Purpose |
| --- | --- |
| 📦 `backups/` | Intended to store your downloaded `.gz` and `.img` VPS backup images. |
| 🗂️ `mounts/` | Alternative directory for mounting disk images locally if you prefer not to use `/tmp`. |
| 📝 `logs/` | For storing command execution logs or debugging output. |
| 🗑️ `tmp/` | A workspace for temporary files generated during unzipping or image inspection. |
| 🐍 `vps_tool/` | The core Python package containing the tool's source code. |

---

## 💻 Commands

Here is a detailed list of all available commands for the CLI:

### Core Configuration
- **`vps-tool init`** 
  Interactively prompts you to enter your VPS IP address and securely saves it to a local `.env` file (which is ignored by Git).
- **`vps-tool edit-ip`**
  Allows you to quickly update or change the currently configured VPS IP address in your `.env` file without opening it manually.

### Backup & Restore (VPS)
- **`vps-tool backup [PATH]`**
  Connects to your VPS and downloads a raw image of your disk (`/dev/sda`). It compresses the data over SSH and saves it locally as a `.gz` file. If `[PATH]` is omitted, it will prompt you interactively for where to save the backup.
- **`vps-tool restore`** 
  *(⚠️ DANGER)* Uploads a local `.gz` backup file back to your VPS and overwrites a target disk block device (defaulting to `/dev/sda`). **You must put your VPS in RESCUE MODE before running this.** It provides a native progress bar during the upload.

### Local Device Management
- **`vps-tool local-backup [PATH]`**
  Creates a `.gz` backup image from a local device (like `/dev/sda` or a USB drive) using `sudo dd` and `gzip`.
- **`vps-tool local-restore`**
  *(⚠️ DANGER)* Writes a `.gz` backup image directly to a local device, completely overwriting it. Uses `sudo` and provides a beautiful native Python progress bar.

### Image Management
- **`vps-tool inspect <image>`**
  Mounts a downloaded `.img` file locally to `/tmp/vps_mount` using `losetup` so you can browse its contents. If you pass a `.gz` file, it will automatically ask if you want to unzip it first.
- **`vps-tool unzip <file>`**
  Takes a compressed `.gz` backup image and extracts it to a raw `.img` file using Python's native gzip. Displays a beautiful real-time progress bar. The original `.gz` is deleted after extraction to save space.
- **`vps-tool zip <file>`**
  Takes an uncompressed raw `.img` file and compresses it back into a `.gz` file. Displays a real-time progress bar and deletes the uncompressed `.img` file after finishing.

### Utility
- **`vps-tool version`**
  Displays the current version of the VPS Imaging Tool.

### Global Options
- **`--help`**
  Displays a helpful menu showing all available commands and options. You can also use this after any command (e.g., `vps-tool backup --help`) for command-specific instructions.
- **`--install-completion`**
  Automatically installs shell auto-completion for your current terminal (bash, zsh, fish, etc.). This allows you to press `TAB` to auto-complete `vps-tool` commands!
- **`--show-completion`**
  Prints the raw shell script for auto-completion so you can manually copy it or add it to your shell configuration file.

---

## ⚠️ WARNING

> [!CAUTION]
> **This tool can overwrite entire disks.**
> **Always use rescue mode** before restoring an image to avoid corrupting the active system!
