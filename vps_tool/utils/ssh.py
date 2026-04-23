from vps_tool.config import VPS_IP

def ssh(cmd: str) -> str:
    return f'ssh root@{VPS_IP} "{cmd}"'
