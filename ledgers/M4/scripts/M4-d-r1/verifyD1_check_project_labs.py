"""Verifier round-1 check of the three project labs (project.html) against their twins.

For each lab: (1) the code block in project.html equals its twin in tests/labs/M4 (lab 2 differs only in the blanks);
(2) the twin runs alone under python -I -W error and its stdout equals the page's expected block; (3) the wall time.
Run from the checkout root: .venv/bin/python -I ledgers/M4/scripts/M4-d-r1/verifyD1_check_project_labs.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGE = ROOT / "course/modules/M/M4/project.html"
TWINS = ROOT / "tests/labs/M4"
PY = ROOT / ".venv/bin/python"


def lab_blocks(text: str, lab_id: str) -> tuple[str, str]:
    section = re.search(rf'<section class="lab[^"]*" id="{lab_id}".*?</section>', text, re.S)
    if section is None:
        raise SystemExit(f"{lab_id}: section not found")
    body = section.group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    if code is None or expected is None:
        raise SystemExit(f"{lab_id}: code or expected block not found")
    return html.unescape(code.group(1)), html.unescape(expected.group(1))


def main() -> int:
    text = PAGE.read_text(encoding="utf-8")
    status = 0
    for n, lab_id in ((1, "lab-M4-project-1"), (2, "lab-M4-project-2"), (3, "lab-M4-project-3")):
        code, expected = lab_blocks(text, lab_id)
        twin = (TWINS / f"lab-M4-project-{n}.py").read_text(encoding="utf-8")
        # The page code and the twin differ only in the final newline (the page's <code> has none); lab 2's blanks are
        # filled from the twin's two return lines before the comparison.
        if n == 2:
            twin_returns = re.findall(r"^    return (.+)$", twin, re.M)
            page_blanks = re.findall(r"^    return ___$", code, re.M)
            print(f"{lab_id}: page holds {len(page_blanks)} blanks ('return ___'); twin returns {twin_returns}")
            filled = code
            for expression in twin_returns[:2]:
                filled = filled.replace("    return ___", f"    return {expression}", 1)
            same = filled.rstrip() == twin.rstrip() and len(page_blanks) == 2
        else:
            same = code.rstrip() == twin.rstrip()
        start = time.perf_counter()
        proc = subprocess.run(
            [str(PY), "-I", "-W", "error", str(TWINS / f"lab-M4-project-{n}.py")],
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        elapsed = time.perf_counter() - start
        printed = proc.stdout
        matches = printed.strip() == expected.strip()
        print(f"{lab_id}: page code == twin: {same}; twin exit {proc.returncode}; stdout == expected: {matches}; {elapsed:.2f}s")
        if proc.returncode != 0 or not matches or not same:
            status = 1
            print("--- stdout:\n" + printed + "--- stderr:\n" + proc.stderr)
            print("--- expected:\n" + expected)
    print("project labs:", "PASS" if status == 0 else "FAIL")
    return status


if __name__ == "__main__":
    sys.exit(main())
