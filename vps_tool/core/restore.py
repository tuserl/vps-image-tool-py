import subprocess
import questionary
from rich.console import Console
from vps_tool.config import VPS_IP, BLOCK_SIZE_RESTORE

console = Console()

def restore_vps():
    console.print("[red]⚠ WARNING: This will overwrite /dev/sda[/red]")

    confirm = questionary.confirm("Are you in RESCUE MODE?").ask()
    if not confirm:
        return

    path = questionary.path("Image file (.gz):").ask()

    cmd = (
        f'gunzip -c "{path}" | '
        f'ssh root@{VPS_IP} "dd of=/dev/sda bs={BLOCK_SIZE_RESTORE} status=progress"'
    )

    subprocess.run(cmd, shell=True)

    console.print("[green]✔ Restore completed[/green]")
