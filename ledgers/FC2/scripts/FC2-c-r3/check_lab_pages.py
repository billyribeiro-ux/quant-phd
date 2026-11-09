"""Verifier check (FC2 slice c, round 3): page code block equals the lab twin, and the expected block equals the twin's stdout.

Run from the checkout root: .venv/bin/python ledgers/FC2/scripts/FC2-c-r3/check_lab_pages.py
"""

from __future__ import annotations

import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {
    "L07": ("course/modules/FC/FC2/L07.html", "tests/labs/FC2/lab-FC2-L07-1.py"),
    "L08": ("course/modules/FC/FC2/L08.html", "tests/labs/FC2/lab-FC2-L08-1.py"),
}
PY = str(ROOT / ".venv" / "bin" / "python")


def main() -> int:
    ok = True
    for lesson, (page_rel, twin_rel) in PAGES.items():
        page = (ROOT / page_rel).read_text(encoding="utf-8")
        twin = (ROOT / twin_rel).read_text(encoding="utf-8")
        code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
        exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
        code = html.unescape(code_m.group(1)) if code_m else None
        expected = html.unescape(exp_m.group(1)) if exp_m else None
        code_equal = code is not None and code.strip() == twin.strip()
        run = subprocess.run(
            [PY, "-I", "-W", "error", str(ROOT / twin_rel)], capture_output=True, text=True, cwd=str(ROOT)
        )
        stdout_equal = expected is not None and expected.strip() == run.stdout.strip()
        print(
            f"{lesson}: code_equal_twin={code_equal} expected_equal_stdout={stdout_equal} "
            f"twin_exit={run.returncode} twin_stderr_bytes={len(run.stderr.encode())}"
        )
        if code is not None and not code_equal:
            for line in difflib.unified_diff(
                twin.strip().splitlines(), code.strip().splitlines(), "twin", "page", lineterm=""
            ):
                print(line)
        if not stdout_equal:
            for line in difflib.unified_diff(
                run.stdout.strip().splitlines(), (expected or "").strip().splitlines(), "stdout", "expected", lineterm=""
            ):
                print(line)
        if not (code_equal and stdout_equal and run.returncode == 0 and not run.stderr):
            ok = False
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
