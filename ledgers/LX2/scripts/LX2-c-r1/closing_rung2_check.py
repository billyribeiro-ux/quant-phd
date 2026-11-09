"""Closing-delta check of the rung 2 claim (project.html line 535, hours table) against the page's own lab 2.

Extracts the lab 2 code and expected block from project.html, fills the two blanks in three ways, runs each
program under python -I -W error, and compares its output with the expected block using the labs.js rule
(whitespace tokens; numbers within tolerance 1e-6 relative; other tokens exact). Prints one line per variant.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
page = (ROOT / "course/modules/LX/LX2/project.html").read_text(encoding="utf-8")
section = page[page.index('id="lab-LX2-project-2"') :]
code_html = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', section, re.S).group(1)
expected_html = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S).group(1)
code = html.unescape(code_html)
expected = html.unescape(expected_html)
assert code.count("hit_rate = ___") == 1 and code.count("bias = ___") == 1, code.count("___")

variants = {
    "page_completed_solution": ("Fraction(hits, horizon)", "Fraction(sum(errors), horizon)"),
    "wrong_hardcoded_same_block": ("Fraction(4, 6)", "Fraction(1, 6)"),
    "wrong_hit_count_over_8": ("Fraction(hits, 8)", "Fraction(sum(errors), horizon)"),
    "wrong_mean_abs_error": ("Fraction(hits, horizon)", "Fraction(sum(abs(e) for e in errors), horizon)"),
}
NUMBER = re.compile(r"^[-+]?\d+(\.\d+)?$")


def same_block(actual: str, exp: str) -> tuple[bool, str]:
    a = actual.strip().split()
    e = exp.strip().split()
    if len(a) != len(e):
        return False, f"token count {len(a)} vs {len(e)}"
    for i, (x, y) in enumerate(zip(a, e)):
        if NUMBER.match(x) and NUMBER.match(y):
            if abs(float(x) - float(y)) > 1e-6 * (1 + abs(float(y))):
                return False, f"token {i + 1}: {x} vs {y}"
        elif x != y:
            return False, f"token {i + 1}: {x!r} vs {y!r}"
    return True, ""


for name, (hit_expr, bias_expr) in variants.items():
    filled = code.replace("hit_rate = ___", "hit_rate = <<HIT>>", 1).replace("bias = ___", "bias = <<BIAS>>", 1)
    filled = filled.replace("<<HIT>>", hit_expr).replace("<<BIAS>>", bias_expr)
    filled = filled.replace("def main() -> None:", "def main() -> None:")
    if "from fractions import Fraction" not in filled:
        raise SystemExit("missing Fraction import")
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "lab2.py"
        f.write_text(filled, encoding="utf-8")
        run = subprocess.run([sys.executable, "-I", "-W", "error", str(f)], capture_output=True, text=True, timeout=60)
    if run.returncode != 0:
        print(f"{name}: RUN ERROR rc={run.returncode} {run.stderr.strip().splitlines()[-1:]}")
        continue
    ok, why = same_block(run.stdout, expected)
    print(f"{name}: hit={hit_expr} bias={bias_expr} -> {'PASSES' if ok else 'FAILS'} {why}")
