import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured.")

if len(sys.argv) != 2:
    print("Usage:")
    print("python scripts/restore_database.py backups/backup.sql")
    sys.exit(1)

backup_file = Path(sys.argv[1])

if not backup_file.exists():
    raise FileNotFoundError(f"{backup_file} does not exist.")

parsed = urlparse(DATABASE_URL)

db_name = parsed.path.lstrip("/")
db_user = parsed.username
db_password = parsed.password
db_host = parsed.hostname
db_port = parsed.port or 5432

env = os.environ.copy()
env["PGPASSWORD"] = db_password or ""

command = [
    "psql",
    "-h",
    db_host,
    "-p",
    str(db_port),
    "-U",
    db_user,
    "-d",
    db_name,
    "-f",
    str(backup_file),
]

print(f"Restoring database from {backup_file}...")

subprocess.run(command, env=env, check=True)

print("Database restored successfully.")
