import os
from dotenv import load_dotenv

load_dotenv()

# Load IP from environment variable, default to a placeholder
VPS_IP = os.getenv("VPS_IP", "127.0.0.1")

BLOCK_SIZE_BACKUP = "64K"
BLOCK_SIZE_RESTORE = "4M"

DEFAULT_MOUNT = "/tmp/vps_mount"
