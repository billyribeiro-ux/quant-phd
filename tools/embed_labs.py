#!/usr/bin/env python3
"""Embed lab code and its real output into a course page (authoring helper).

A builder writes each lab once, as its local twin ``tests/labs/<UNIT>/<lab-id>.py``,
and puts two markers in the page:

    <pre><code class="language-python" data-run>@@LAB:<lab-id>.py@@</code></pre>
    <pre class="expected" data-tolerance="1e-6">@@OUT:<lab-id>.py@@</pre>

This tool replaces ``@@LAB`` with the twin's HTML-escaped source (so page and twin
are byte-identical after unescaping) and ``@@OUT`` with the output the twin
actually prints under ``python -I -W error``. Expected outputs are therefore never
typed by hand. Pages without markers are left untouched; run_labs.py then keeps
page and twin in agreement.

Usage::

    python3 tools/embed_labs.py course/modules/S/S7/L01.html [more pages...]
"""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKER = re.compile(r"@@(LAB|OUT):([A-Za-z0-9_.-]+\.py)@@")


def run_twin(path: Path) -> str:
    result = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(path)],
        capture_output=True,
        text=True,
        timeout=300,
        check=False,
    )
    if result.returncode != 0 or result.stderr:
        raise RuntimeError(f"{path.name} failed or wrote to stderr:\n{result.stderr}")
    return result.stdout.rstrip("\n")


def embed(page: Path) -> int:
    unit = re.search(r'data-unit="([^"]+)"', page.read_text(encoding="utf-8"))
    if not unit:
        raise RuntimeError(f"{page}: <html> has no data-unit")
    twins = ROOT / "tests" / "labs" / unit.group(1)
    text = page.read_text(encoding="utf-8")
    outputs: dict[str, str] = {}

    def replace(match: re.Match[str]) -> str:
        kind, name = match.group(1), match.group(2)
        twin = twins / name
        if not twin.exists():
            raise RuntimeError(f"{page.name}: no twin {twin.relative_to(ROOT)}")
        if kind == "LAB":
            return html.escape(twin.read_text(encoding="utf-8").rstrip("\n"), quote=False)
        if name not in outputs:
            outputs[name] = run_twin(twin)
        return html.escape(outputs[name], quote=False)

    new, count = MARKER.subn(replace, text)
    if count:
        page.write_text(new, encoding="utf-8")
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pages", nargs="+", type=Path)
    args = parser.parse_args()
    try:
        for page in args.pages:
            print(f"{page}: embedded {embed(page)} markers")
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
