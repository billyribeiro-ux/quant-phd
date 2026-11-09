"""Closing-round harness (LX2-c round 1): run every lab-2 mutant and alternative and apply the labs.js compare rule.

Rule (course/assets/js/labs.js compareOutput, read in this checkout): tokens split on whitespace; a token pair where
both sides match NUMBER agrees when |actual - expected| <= tol * (1 + |expected|); every other token must be identical.
The expected block is read from course/modules/LX/LX2/project.html (pre.expected of section lab-LX2-project-2).
A mutant is KILLED when the compare fails or the run exits non-zero; SURVIVES otherwise.
Run from the checkout root: .venv/bin/python ledgers/LX2/scripts/LX2-c-r1/lab2_harness_r1.py
"""

from __future__ import annotations

import glob
import html
import os
import re
import subprocess
import sys

ROOT = os.getcwd()
NUMBER = re.compile(r"^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?%?$")


def expected_block() -> tuple[str, float]:
    text = open(os.path.join(ROOT, "course/modules/LX/LX2/project.html"), encoding="utf-8").read()
    start = text.index('id="lab-LX2-project-2"')
    m = re.search(r'<pre class="expected" data-tolerance="([^"]+)">(.*?)</pre>', text[start:], re.S)
    assert m, "expected block not found"
    return html.unescape(m.group(2)), float(m.group(1))


def compare(actual: str, expected: str, tol: float) -> tuple[bool, str]:
    a = actual.strip().split()
    e = expected.strip().split()
    if len(a) != len(e):
        return False, f"expected {len(e)} tokens, got {len(a)}"
    for i, (x_s, y_s) in enumerate(zip(a, e, strict=True)):
        if NUMBER.match(y_s) and NUMBER.match(x_s):
            x = float(x_s.rstrip("%"))
            y = float(y_s.rstrip("%"))
            if not abs(x - y) <= tol * (1 + abs(y)):
                return False, f"token {i + 1}: {x_s} vs {y_s}"
        elif x_s != y_s:
            return False, f'token {i + 1}: "{x_s}" vs "{y_s}"'
    return True, ""


def main() -> int:
    expected, tol = expected_block()
    files = sorted(glob.glob(os.path.join(ROOT, "ledgers/LX2/mutants/*lab2*.py")))
    print(f"files {len(files)}")
    killed = []
    survived = []
    for path in files:
        name = os.path.basename(path)
        proc = subprocess.run(
            [sys.executable, "-I", "-W", "error", path],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        ok, reason = compare(proc.stdout, expected, tol)
        status = "SURVIVES" if (ok and proc.returncode == 0) else "KILLED"
        detail = reason if status == "KILLED" else ""
        if proc.returncode != 0:
            detail = f"exit {proc.returncode}; stderr {proc.stderr.strip()[:120]!r}"
        print(f"{status:8} {name} {detail}")
        (killed if status == "KILLED" else survived).append(name)
    print(f"KILLED {len(killed)}  SURVIVED {len(survived)}")
    print("SURVIVORS:")
    for name in survived:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
