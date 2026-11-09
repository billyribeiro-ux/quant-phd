"""SC1-a round 20: run every lab-twin mutant under python -I -W error and compare its stdout with the expected block
of the page that embeds the twin (rule of labs.js: numbers within tol*(1+|expected|), other tokens exact).

A mutant is killed when it exits non-zero, writes to stderr, or its output differs from the page's expected block.
Usage (from the checkout root): python3 -I ledgers/SC1/scripts/SC1-a-r20/kill_lab_mutants_r20.py
"""

import glob
import html
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
PY = os.path.join(ROOT, ".venv", "bin", "python")
NUM = re.compile(r"^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?%?$")


def expected_block(lab: str) -> tuple[str, float]:
    page = os.path.join(ROOT, "course", "modules", "SC", "SC1", f"{lab}.html")
    text = open(page, encoding="utf-8").read()
    m = re.search(r'<pre class="expected" data-tolerance="([^"]+)">(.*?)</pre>', text, re.S)
    assert m, lab
    return html.unescape(m.group(2)), float(m.group(1))


def compare(actual: str, expected: str, tol: float) -> tuple[bool, str]:
    a, e = actual.split(), expected.split()
    if len(a) != len(e):
        return False, f"token count {len(a)} vs {len(e)}"
    for i, (x, y) in enumerate(zip(a, e, strict=True)):
        if NUM.match(x) and NUM.match(y):
            if not abs(float(x.rstrip("%")) - float(y.rstrip("%"))) <= tol * (1 + abs(float(y.rstrip("%")))):
                return False, f"token {i + 1}: {x} vs {y}"
        elif x != y:
            return False, f"token {i + 1}: {x!r} vs {y!r}"
    return True, ""


def main() -> int:
    files = sorted(glob.glob(os.path.join(ROOT, "ledgers", "SC1", "lab-mutants", "**", "*.py"), recursive=True))
    killed = 0
    survivors = []
    for path in files:
        name = os.path.basename(path)
        m = re.search(r"L0([1-3])", name)
        if not m:
            print(f"SKIP {name}: no lab id in name")
            continue
        lab = f"L0{m.group(1)}"
        expected, tol = expected_block(lab)
        with tempfile.TemporaryDirectory() as work:
            proc = subprocess.run(
                [PY, "-I", "-W", "error", path], cwd=work, capture_output=True, text=True, timeout=120
            )
        if proc.returncode != 0 or proc.stderr.strip():
            killed += 1
            print(f"KILLED {os.path.relpath(path, ROOT)} ({lab}): rc={proc.returncode} stderr={proc.stderr.strip()[:120]!r}")
            continue
        ok, why = compare(proc.stdout, expected, tol)
        if ok:
            survivors.append(os.path.relpath(path, ROOT))
            print(f"SURVIVED {os.path.relpath(path, ROOT)} ({lab})")
        else:
            killed += 1
            print(f"KILLED {os.path.relpath(path, ROOT)} ({lab}): {why}")
    print(f"lab mutants killed {killed}/{killed + len(survivors)}; survivors {len(survivors)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
