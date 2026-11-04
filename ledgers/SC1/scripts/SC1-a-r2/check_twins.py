"""Round-2 verifier check for SC1 slice a: page code equals twin, expected block equals twin output.

Run from the checkout root: .venv/bin/python ledgers/SC1/scripts/SC1-a-r2/check_twins.py
Runs each twin as `python -I -W error <twin>` and compares stdout with the expected block of its page.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {
    "L01": ROOT / "course/modules/SC/SC1/L01.html",
    "L02": ROOT / "course/modules/SC/SC1/L02.html",
    "L03": ROOT / "course/modules/SC/SC1/L03.html",
}
CODE_RE = re.compile(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', re.S)
EXPECTED_RE = re.compile(r'<pre class="expected"[^>]*>(.*?)</pre>', re.S)


def main() -> int:
    status = 0
    for page, path in PAGES.items():
        text = path.read_text(encoding="utf-8")
        codes = CODE_RE.findall(text)
        expecteds = EXPECTED_RE.findall(text)
        twin = ROOT / f"tests/labs/SC1/lab-SC1-{page}-1.py"
        twin_src = twin.read_text(encoding="utf-8")
        page_code = html.unescape(codes[0])
        same = page_code == twin_src
        print(f"{page}: code blocks={len(codes)} expected blocks={len(expecteds)} page code == twin: {same}")
        if not same:
            status = 1
            import difflib

            for line in difflib.unified_diff(
                twin_src.splitlines(), page_code.splitlines(), "twin", "page", lineterm=""
            ):
                print("   ", line)
        run = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, check=False
        )
        print(f"{page}: twin exit={run.returncode} stderr_bytes={len(run.stderr.encode())}")
        expected = html.unescape(expecteds[0]).rstrip("\n")
        got = run.stdout.rstrip("\n")
        eq = expected == got
        print(f"{page}: expected block == twin stdout: {eq} ({len(got.splitlines())} lines)")
        if run.returncode != 0 or not eq:
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
