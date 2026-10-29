"""Verifier check (E5 slice b, round 5): lab twins L04-L06.

For each lesson page: extract the data-run code block and the expected block, unescape HTML,
check that the page code equals the twin file, run the twin alone under python -I -W error from a
scratch cwd, and check that the expected block equals the captured stdout.
Run from the checkout root: .venv/bin/python ledgers/E5/scripts/E5-b-r5/check_labs_b_r5.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {
    "L04": ("course/modules/E/E5/L04.html", "tests/labs/E5/lab-E5-L04-1.py"),
    "L05": ("course/modules/E/E5/L05.html", "tests/labs/E5/lab-E5-L05-1.py"),
    "L06": ("course/modules/E/E5/L06.html", "tests/labs/E5/lab-E5-L06-1.py"),
}
SCRATCH = Path("/tmp/e5b_r5_scratch")


def main() -> int:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    ok_all = True
    for page_id, (page_rel, twin_rel) in PAGES.items():
        text = (ROOT / page_rel).read_text(encoding="utf-8")
        code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
        exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
        if not code_m or not exp_m:
            print(page_id, "MISSING BLOCK")
            ok_all = False
            continue
        page_code = html.unescape(code_m.group(1))
        expected = html.unescape(exp_m.group(1))
        twin = (ROOT / twin_rel).read_text(encoding="utf-8")
        page_equals_twin = page_code.strip("\n") == twin.strip("\n")
        # run twin alone, plain CPython, isolated, warnings as errors, from a scratch cwd
        proc = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(ROOT / twin_rel)],
            cwd=str(SCRATCH),
            capture_output=True,
            text=True,
            timeout=60,
        )
        stdout = proc.stdout
        expected_equals_output = expected.strip() == stdout.strip()
        print(
            page_id,
            f"exit={proc.returncode}",
            f"page_code_equals_twin={page_equals_twin}",
            f"expected_equals_output={expected_equals_output}",
            f"stderr={proc.stderr.strip()!r}",
        )
        if proc.returncode != 0 or not page_equals_twin or not expected_equals_output:
            ok_all = False
            if not expected_equals_output:
                diff_lines = [
                    f"  exp: {a!r}\n  out: {b!r}"
                    for a, b in zip(expected.strip().splitlines(), stdout.strip().splitlines())
                    if a != b
                ]
                print("\n".join(diff_lines[:5]))
    print("ALL_OK" if ok_all else "FAILED")
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
