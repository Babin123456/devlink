from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]

backup_dir = ROOT / "backups"
backup_dir.mkdir(exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

archive = backup_dir / f"storage_backup_{timestamp}.zip"

storage_dirs = [
    ROOT / "uploads",
]

found = False

with ZipFile(archive, "w", ZIP_DEFLATED) as zipf:
    for directory in storage_dirs:
        if directory.exists():
            found = True

            for file in directory.rglob("*"):
                if file.is_file():
                    zipf.write(file, file.relative_to(ROOT))

if found:
    print(f"Storage backup created: {archive}")
else:
    print("No storage directories found to back up.")
