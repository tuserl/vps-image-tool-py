import typer
import questionary
from dotenv import set_key
from vps_tool.core.backup import backup_vps
from vps_tool.core.restore import restore_vps
from vps_tool.core.local import local_backup, local_restore
from vps_tool.core.inspect import inspect_image
from vps_tool.utils.files import unzip_file, zip_file

app = typer.Typer(help="VPS Imaging Tool")


@app.command()
def backup(path: str = typer.Argument(None, help="Optional path to save the .gz image")):
    """Backup VPS disk"""
    backup_vps(path)


@app.command()
def restore():
    """Restore VPS disk (DANGER)"""
    restore_vps()


@app.command("local-backup")
def cli_local_backup(path: str = typer.Argument(None, help="Optional path to save the .gz image")):
    """Backup a LOCAL disk"""
    local_backup(path)


@app.command("local-restore")
def cli_local_restore():
    """Restore an image to a LOCAL disk (DANGER)"""
    local_restore()


@app.command()
def inspect(path: str):
    """Inspect disk image"""
    inspect_image(path)


@app.command()
def unzip(path: str):
    """Unzip .gz image"""
    unzip_file(path)


@app.command()
def zip(path: str):
    """Zip an .img file into .gz"""
    zip_file(path)


@app.command()
def init():
    """Initialize configuration (.env file)"""
    ip = questionary.text("Enter your VPS IP address:").ask()
    if ip:
        with open(".env", "w") as f:
            f.write(f"VPS_IP={ip}\n")
        print(f"✅ Configuration saved to .env with IP: {ip}")
    else:
        print("❌ Initialization cancelled.")


@app.command()
def edit_ip():
    """Edit the configured VPS IP address"""
    from vps_tool.config import VPS_IP
    new_ip = questionary.text("Enter new VPS IP address:", default=VPS_IP or "").ask()
    if new_ip:
        set_key(".env", "VPS_IP", new_ip)
        print(f"✅ IP address updated to: {new_ip}")
    else:
        print("❌ Update cancelled.")


@app.command()
def version():
    print("vps-tool v1.0")


if __name__ == "__main__":
    app()
