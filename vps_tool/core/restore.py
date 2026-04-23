import subprocess
import questionary
from rich.console import Console
from vps_tool.config import VPS_IP, BLOCK_SIZE_RESTORE

console = Console()

def restore_vps():
    target_dev = questionary.text("Target device on VPS to overwrite:", default="/dev/sda").ask()
    if not target_dev:
        return

    console.print(f"[red]⚠ WARNING: This will overwrite {target_dev}[/red]")

    confirm = questionary.confirm("Are you in RESCUE MODE?").ask()
    if not confirm:
        return

    path = questionary.path("Image file (.gz):").ask()
    if not path:
        return

    cmd = (
        f'gunzip -c "{path}" | '
        f'ssh root@{VPS_IP} "dd of={target_dev} bs={BLOCK_SIZE_RESTORE} status=progress"'
    )

    subprocess.run(cmd, shell=True)

    console.print("[green]✔ Restore completed[/green]")
