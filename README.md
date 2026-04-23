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

Before using the tool, you must configure your VPS IP address. Open `vps_tool/config.py` and set your server's IP:

```python
VPS_IP = "139.177.195.158"  # Replace with your actual VPS IP
```

---

## 📖 User Manual

### 💾 Where are images stored?
By default, running `vps-tool backup` pipes the disk image over SSH and saves the resulting `.gz` file directly into your **current working directory** (wherever you run the command from).

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

Here are the available commands for the CLI:

- `vps-tool backup` — Backup your VPS disk
- `vps-tool restore` — Restore your VPS disk (**DANGER**)
- `vps-tool inspect <image>` — Inspect a downloaded disk image
- `vps-tool unzip <file>` — Unzip a `.gz` image file

---

## ⚠️ WARNING

> [!CAUTION]
> **This tool can overwrite entire disks.**
> **Always use rescue mode** before restoring an image to avoid corrupting the active system!
