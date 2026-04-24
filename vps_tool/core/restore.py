import subprocess
import questionary
import os
import gzip
from rich.console import Console
from rich.progress import Progress
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

    cmd = f'ssh root@{VPS_IP} "dd of={target_dev} bs={BLOCK_SIZE_RESTORE} status=progress"'
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)

    total_size = os.path.getsize(path)
    
    try:
        with open(path, 'rb') as f_in:
            with Progress() as progress:
                task = progress.add_task(f"[cyan]Restoring {path}...", total=total_size)
                
                decompressor = gzip.GzipFile(fileobj=f_in)
                chunk_size = 1024 * 1024 * 4  # 4MB chunks
                
                while True:
                    chunk = decompressor.read(chunk_size)
                    if not chunk:
                        break
                    process.stdin.write(chunk)
                    progress.update(task, completed=f_in.tell())
    except Exception as e:
        console.print(f"[red]Error during restore: {e}[/red]")
    finally:
        process.stdin.close()
        process.wait()

    console.print("[green]✔ Restore completed[/green]")
