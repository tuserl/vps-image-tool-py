import os

def resolve(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))
