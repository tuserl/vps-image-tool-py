import subprocess
from rich.console import Console

console = Console()

def unzip_file(path: str):
    subprocess.run(f"gunzip -v {path}", shell=True)
    console.print("[green]✔ Unzipped[/green]")
