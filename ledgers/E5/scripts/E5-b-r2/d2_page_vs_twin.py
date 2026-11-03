"""Round 2 verifier check (E5-b): page lab code equals its twin, twin runs under -I -W error, expected block equals output.

Run from the repository root with the repo venv: .venv/bin/python ledgers/E5/scripts/E5-b-r2/d2_page_vs_twin.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {
    "L04": ROOT / "course/modules/E/E5/L04.html",
    "L05": ROOT / "course/modules/E/E5/L05.html",
    "L06": ROOT / "course/modules/E/E5/L06.html",
}
TWINS = {
    "L04": ROOT / "tests/labs/E5/lab-E5-L04-1.py",
    "L05": ROOT / "tests/labs/E5/lab-E5-L05-1.py",
    "L06": ROOT / "tests/labs/E5/lab-E5-L06-1.py",
}

CODE_RE = re.compile(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', re.S)
EXP_RE = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)


def main() -> int:
    failures = 0
    for page, path in PAGES.items():
        text = path.read_text(encoding="utf-8")
        codes = CODE_RE.findall(text)
        expected = EXP_RE.findall(text)
        twin = TWINS[page].read_text(encoding="utf-8")
        code = html.unescape(codes[0]) if len(codes) == 1 else ""
        exp = html.unescape(expected[0]) if len(expected) == 1 else ""
        print(f"{page}: code_blocks={len(codes)} expected_blocks={len(expected)}")
        same_code = code.rstrip("\n") == twin.rstrip("\n")
        print(f"{page}: page code equals twin (rstrip newline): {same_code}")
        if not same_code:
            failures += 1
        with tempfile.TemporaryDirectory() as work:
            result = subprocess.run(
                [sys.executable, "-I", "-W", "error", str(TWINS[page])],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
                env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"},
                cwd=work,
            )
        print(f"{page}: twin exit={result.returncode} stderr_bytes={len(result.stderr)}")
        out = result.stdout
        same_out = out.rstrip("\n") == exp.rstrip("\n")
        print(f"{page}: expected block equals twin stdout (exact): {same_out}")
        if result.returncode != 0 or result.stderr or not same_out:
            failures += 1
            if not same_out:
                diff = [
                    (i, a, b)
                    for i, (a, b) in enumerate(zip(out.splitlines(), exp.splitlines()))
                    if a != b
                ]
                print(f"{page}: differing lines (index, output, expected): {diff}")
                print(f"{page}: output line count {len(out.splitlines())}, expected {len(exp.splitlines())}")
    print(f"FAILURES {failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
