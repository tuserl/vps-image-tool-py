import os
import gzip
from rich.console import Console
from rich.progress import Progress

console = Console()

def unzip_file(path: str):
    out_path = path[:-3] if path.endswith('.gz') else path + '.unzipped'
    total_size = os.path.getsize(path)
    
    with open(path, 'rb') as f_in, open(out_path, 'wb') as f_out:
        with Progress() as progress:
            task = progress.add_task(f"[cyan]Unzipping {path}...", total=total_size)
            
            decompressor = gzip.GzipFile(fileobj=f_in)
            chunk_size = 1024 * 1024  # 1MB chunks
            
            while True:
                chunk = decompressor.read(chunk_size)
                if not chunk:
                    break
                f_out.write(chunk)
                progress.update(task, completed=f_in.tell())
                
    os.remove(path)
    console.print(f"[green]✔ Unzipped to {out_path}[/green]")
