import subprocess
from rich.console import Console
from vps_tool.config import VPS_IP, BLOCK_SIZE_BACKUP

console = Console()

def backup_vps():
    console.print("[cyan]Starting VPS backup...[/cyan]")

    cmd = (
        f'ssh root@{VPS_IP} '
        f'"dd if=/dev/sda bs={BLOCK_SIZE_BACKUP} status=progress | gzip -1"'
    )

    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    console.print("[green]✔ Backup completed[/green]")
