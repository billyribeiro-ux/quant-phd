"""SC1 slice a, round 9: independent check of the L01-L03 lab twins against their pages.

For each lab section in L01.html, L02.html, L03.html:
  * the <code class="language-python" data-run> text, HTML-unescaped, must equal the twin file exactly;
  * each twin runs as `python -I -W error <twin>` from an empty scratch directory (exit 0, empty stderr);
  * the stdout must equal the page's <pre class="expected"> text exactly (tolerance is 0 for these tokens).

Usage (from the checkout root): .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r9/twin_check.py
Prints one line per lab and a final summary.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGE_DIR = ROOT / "course" / "modules" / "SC" / "SC1"
TWIN_DIR = ROOT / "tests" / "labs" / "SC1"

SECTION_RE = re.compile(r'<section class="lab" id="(?P<id>lab-SC1-L0\d-1)".*?</section>', re.S)
CODE_RE = re.compile(r'<code class="language-python" data-run>(?P<code>.*?)</code>', re.S)
EXPECTED_RE = re.compile(r'<pre class="expected"[^>]*>(?P<out>.*?)</pre>', re.S)


def main() -> int:
    failures = 0
    for page in ("L01", "L02", "L03"):
        text = (PAGE_DIR / f"{page}.html").read_text(encoding="utf-8")
        for m in SECTION_RE.finditer(text):
            lab_id = m.group("id")
            body = m.group(0)
            code = html.unescape(CODE_RE.search(body).group("code"))  # type: ignore[union-attr]
            expected = html.unescape(EXPECTED_RE.search(body).group("out"))  # type: ignore[union-attr]
            twin_path = TWIN_DIR / f"{lab_id}.py"
            twin = twin_path.read_text(encoding="utf-8")
            code_equal = code.rstrip("\n") == twin.rstrip("\n")
            with tempfile.TemporaryDirectory(prefix="sc1r9-") as scratch:
                started = time.perf_counter()
                result = subprocess.run(
                    [sys.executable, "-I", "-W", "error", str(twin_path)],
                    cwd=scratch,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    check=False,
                    env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"},
                )
                elapsed = time.perf_counter() - started
            out_equal = result.stdout.rstrip("\n") == expected.rstrip("\n")
            ok = code_equal and result.returncode == 0 and result.stderr == "" and out_equal
            failures += not ok
            print(
                f"{lab_id}: code_equal_twin={code_equal} exit={result.returncode} stderr_bytes={len(result.stderr)} "
                f"expected_equal_stdout={out_equal} cpython_seconds={elapsed:.3f} -> {'OK' if ok else 'MISMATCH'}"
            )
            if not out_equal:
                print("--- stdout ---")
                print(result.stdout)
                print("--- expected ---")
                print(expected)
            if not code_equal:
                print(f"code length page={len(code)} twin={len(twin)}")
    print(f"twin_check: {'PASS' if failures == 0 else 'FAIL'} (failures={failures})")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
