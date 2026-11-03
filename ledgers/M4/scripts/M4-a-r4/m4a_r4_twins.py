"""Round-4 check for M4 slice a: page code equals twin, page expected block equals twin stdout.

Run from the checkout root with the project venv: .venv/bin/python ledgers/M4/scripts/M4-a-r4/m4a_r4_twins.py
Each twin is executed with `python -I -W error` from an empty scratch directory (no data/ directory).
The page blocks are read as text; HTML entities are decoded before comparison.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PY = ROOT / ".venv" / "bin" / "python"
PAGES = {"L01": "lab-M4-L01-1", "L02": "lab-M4-L02-1", "L03": "lab-M4-L03-1", "L04": "lab-M4-L04-1"}


def page_blocks(page: Path) -> tuple[str, str, int]:
    text = page.read_text(encoding="utf-8")
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    if not code_m or not exp_m:
        raise SystemExit(f"{page}: lab block not found")
    return html.unescape(code_m.group(1)), html.unescape(exp_m.group(1)), text.count("class=\"lab")


def main() -> int:
    ok = True
    for page_id, twin_id in PAGES.items():
        page = ROOT / "course" / "modules" / "M" / "M4" / f"{page_id}.html"
        twin = ROOT / "tests" / "labs" / "M4" / f"{twin_id}.py"
        code, expected, _ = page_blocks(page)
        twin_src = twin.read_text(encoding="utf-8")
        same_code = code.strip("\n") == twin_src.strip("\n")
        with tempfile.TemporaryDirectory() as scratch:
            run = subprocess.run(
                [str(PY), "-I", "-W", "error", str(twin)],
                cwd=scratch,
                capture_output=True,
                text=True,
                timeout=60,
            )
        same_out = run.stdout.rstrip("\n") == expected.rstrip("\n")
        print(
            f"{page_id} twin={twin.relative_to(ROOT)} exit={run.returncode} stderr_bytes={len(run.stderr)} "
            f"page_code_equals_twin={same_code} expected_equals_stdout={same_out} "
            f"stdout_lines={len(run.stdout.splitlines())} expected_lines={len(expected.splitlines())}"
        )
        if run.returncode != 0 or run.stderr or not same_code or not same_out:
            ok = False
            print(run.stderr)
            print("--- stdout ---")
            print(run.stdout)
            print("--- expected ---")
            print(expected)
        if not same_code:
            import difflib

            print("".join(difflib.unified_diff(twin_src.splitlines(True), code.splitlines(True), "twin", "page")))
    print("twins PASS" if ok else "twins FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
