"""
Export the DevLink FastAPI OpenAPI schema to a JSON file for SDK generation.

Usage:
    python scripts/export_openapi.py [output_path]

The output path defaults to ``../clients/openapi.json`` (relative to this
script's ``backend`` directory).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.main import app


def main() -> None:
    output = (
        Path(sys.argv[1]).resolve()
        if len(sys.argv) > 1
        else Path(__file__).resolve().parents[1] / "clients" / "openapi.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)

    schema = app.openapi()
    schema["info"] = {
        "title": "DevLink API",
        "version": app.version,
    }

    output.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print(f"OpenAPI schema written to {output}")


if __name__ == "__main__":
    main()
