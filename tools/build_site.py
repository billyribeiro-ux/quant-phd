#!/usr/bin/env python3
"""Publish generated data into the static site and check it is servable.

Copies the validated curriculum and the verified citation registry into
``course/assets/data/`` (trimmed to what pages need), then checks that every
vendored runtime file is present and unmodified. The site under ``course/``
has no build framework: after this step it can be served by any static file
server, e.g. ``python3 -m http.server -d course``.

Usage::

    python3 tools/build_site.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "course" / "assets" / "data"
REF_FIELDS = ("key", "doi", "type", "title", "authors", "year", "container", "volume", "issue", "pages", "isbn")


def _run(*args: str) -> None:
    result = subprocess.run([sys.executable, *args], cwd=ROOT, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def publish_references() -> int:
    registry: dict[str, Any] = json.loads((ROOT / "references" / "references.json").read_text(encoding="utf-8"))
    slim = {
        e["key"]: {field: e[field] for field in REF_FIELDS if e.get(field) not in (None, "", [])}
        for e in registry["entries"]
    }
    (DATA / "references.json").write_text(
        json.dumps({"count": len(slim), "entries": slim}, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    return len(slim)


def main() -> int:
    _run("tools/render_curriculum.py")
    _run("tools/vendor.py", "check")
    DATA.mkdir(parents=True, exist_ok=True)
    curriculum = (ROOT / "curriculum" / "curriculum.json").read_text(encoding="utf-8")
    (DATA / "curriculum.json").write_text(curriculum, encoding="utf-8")
    count = publish_references()
    print(f"site data published: curriculum.json, references.json ({count} entries) -> {DATA.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
