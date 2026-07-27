import os
import subprocess
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured.")

ROOT = Path(__file__).resolve().parents[1]

backup_dir = ROOT / "backups"
backup_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = backup_dir / f"devlink_backup_{timestamp}.sql"

parsed = urlparse(DATABASE_URL)

db_name = parsed.path.lstrip("/")
db_user = parsed.username
db_password = parsed.password
db_host = parsed.hostname
db_port = parsed.port or 5432

env = os.environ.copy()
env["PGPASSWORD"] = db_password or ""

command = [
    "pg_dump",
    "-h", db_host,
    "-p", str(db_port),
    "-U", db_user,
    "-F", "p",
    "-f", str(backup_file),
    db_name,
]

print("Creating database backup...")

subprocess.run(command, env=env, check=True)

print(f"Backup created: {backup_file}")