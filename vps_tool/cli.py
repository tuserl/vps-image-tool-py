import typer
from vps_tool.core.backup import backup_vps
from vps_tool.core.restore import restore_vps
from vps_tool.core.inspect import inspect_image
from vps_tool.utils.files import unzip_file

app = typer.Typer(help="VPS Imaging Tool")


@app.command()
def backup():
    """Backup VPS disk"""
    backup_vps()


@app.command()
def restore():
    """Restore VPS disk (DANGER)"""
    restore_vps()


@app.command()
def inspect(path: str):
    """Inspect disk image"""
    inspect_image(path)


@app.command()
def unzip(path: str):
    """Unzip .gz image"""
    unzip_file(path)


@app.command()
def version():
    print("vps-tool v1.0")


if __name__ == "__main__":
    app()
