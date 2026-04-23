import subprocess
import questionary
from rich.console import Console
from vps_tool.config import VPS_IP, BLOCK_SIZE_BACKUP

console = Console()

def backup_vps(save_path: str = None):
    if not save_path:
        save_path = questionary.path("Save image to (.gz):", default="backup.img.gz").ask()
        
    if not save_path:
        return

    console.print(f"[cyan]Starting VPS backup to {save_path}...[/cyan]")

    cmd = (
        f'ssh root@{VPS_IP} '
        f'"dd if=/dev/sda bs={BLOCK_SIZE_BACKUP} status=progress | gzip -1" > "{save_path}"'
    )

    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    console.print("[green]✔ Backup completed[/green]")
