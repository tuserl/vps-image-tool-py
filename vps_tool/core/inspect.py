import subprocess
import questionary
from rich.console import Console
from vps_tool.config import DEFAULT_MOUNT
from vps_tool.utils.files import unzip_file

console = Console()

def inspect_image(path: str):
    if path.endswith(".gz"):
        unzip = questionary.confirm("This is a compressed (.gz) file. Do you want to unzip it first?").ask()
        if unzip:
            console.print(f"[cyan]Unzipping {path}...[/cyan]")
            unzip_file(path)
            path = path[:-3]  # Remove .gz extension
        else:
            console.print("[red]Cannot inspect a compressed file without unzipping. Exiting.[/red]")
            return

    subprocess.run(f"sudo losetup -fP {path}", shell=True)

    loop = subprocess.getoutput(f"losetup -j {path} | cut -d: -f1").strip()

    console.print(f"[cyan]Loop device: {loop}[/cyan]")

    parts = subprocess.getoutput(
        f"lsblk -ln -o NAME {loop}"
    ).splitlines()

    if len(parts) <= 1:
        console.print("[yellow]No partitions found, mounting raw device[/yellow]")
        selected = loop
    else:
        for i, p in enumerate(parts):
            console.print(f"[{i}] /dev/{p}")

        idx = int(questionary.text("Select partition index:").ask())
        selected = "/dev/" + parts[idx]

    subprocess.run(f"sudo mkdir -p {DEFAULT_MOUNT}", shell=True)
    subprocess.run(f"sudo mount {selected} {DEFAULT_MOUNT}", shell=True)

    console.print(f"[green]Mounted at {DEFAULT_MOUNT}[/green]")

    input("Press ENTER to unmount...")

    subprocess.run(f"sudo umount {DEFAULT_MOUNT}", shell=True)
    subprocess.run(f"sudo losetup -d {loop}", shell=True)
