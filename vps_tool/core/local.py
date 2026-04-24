import os
import gzip
import subprocess
import questionary
from rich.console import Console
from rich.progress import Progress
from vps_tool.config import BLOCK_SIZE_BACKUP, BLOCK_SIZE_RESTORE

console = Console()

def local_backup(save_path: str = None):
    source_dev = questionary.text("Local device to backup:", default="/dev/sda").ask()
    if not source_dev:
        return

    if not save_path:
        save_path = questionary.path("Save image to (.gz):", default="local-backup.img.gz").ask()
        if not save_path:
            return

    console.print(f"[cyan]Starting local backup from {source_dev} to {save_path}...[/cyan]")

    # Using sudo because reading a raw block device requires root privileges
    cmd = f'sudo dd if={source_dev} bs={BLOCK_SIZE_BACKUP} status=progress | gzip -1 > "{save_path}"'
    subprocess.run(cmd, shell=True)

    console.print("[green]✔ Local backup completed[/green]")

def local_restore():
    target_dev = questionary.text("Local device to overwrite:", default="/dev/sda").ask()
    if not target_dev:
        return

    console.print(f"[red]⚠ WARNING: This will completely OVERWRITE {target_dev} on your local machine![/red]")
    confirm = questionary.confirm("Are you absolutely sure?").ask()
    if not confirm:
        return

    path = questionary.path("Image file (.gz):").ask()
    if not path:
        return

    # Force sudo to ask for password now, so it doesn't interrupt our Python subprocess stdin pipe
    subprocess.run("sudo -v", shell=True)

    cmd = f'sudo dd of={target_dev} bs={BLOCK_SIZE_RESTORE} status=progress'
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE)

    total_size = os.path.getsize(path)
    
    try:
        with open(path, 'rb') as f_in:
            with Progress() as progress:
                task = progress.add_task(f"[cyan]Restoring {path} to {target_dev}...", total=total_size)
                
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

    console.print("[green]✔ Local restore completed[/green]")
