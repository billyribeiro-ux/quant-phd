"""Kill check for SC1 lab twins (round 11, slice a).

For each twin, run the unmutated twin and the mutant under python -I -W error in a scratch directory, and compare
each stdout with the expected block of the page (the same text the page shows). A mutant is KILLED when its stdout
differs from the expected block. The baseline must match the expected block exactly.
"""

from __future__ import annotations

import html
import os
import re
import subprocess
import sys
import tempfile

REPO = "/Users/billyribeiro/.fanout/wt/verifyE11-SC1-a"
PAGES = {
    "L01": f"{REPO}/course/modules/SC/SC1/L01.html",
    "L02": f"{REPO}/course/modules/SC/SC1/L02.html",
    "L03": f"{REPO}/course/modules/SC/SC1/L03.html",
}
TWINS = {k: f"{REPO}/tests/labs/SC1/lab-SC1-{k}-1.py" for k in PAGES}
MUT_DIR = f"{REPO}/ledgers/SC1/mutants/SC1-a-r11"

MUTANTS = {
    "m1-L01-coverage-uses-max-index": (
        "L01",
        "return sum(variances[: min(i, j)], Fraction(0))",
        "return sum(variances[: max(i, j)], Fraction(0))",
        "Covariance sums the increments up to the larger time, not the smaller; the 81 of 81 count must drop.",
    ),
    "m2-L02-hat-support-doubled": (
        "L02",
        "return max(0.0, 1.0 - 2.0**m * abs(t - centre))",
        "return max(0.0, 1.0 - 2.0 ** (m - 1) * abs(t - centre))",
        "Hat support has radius 2**(-(m-1)) instead of 2**(-m); the dyadic-fixed count and the grid check must move.",
    ),
    "m3-L02-grid-depth-too-coarse": (
        "L02",
        "GRID_DEPTH = 10",
        "GRID_DEPTH = 3",
        "Grid of 2**-3 misses hat centres of level 4 and above, so the grid-supremum line must print False.",
    ),
    "m4-L03-se-divisor-n": (
        "L03",
        "return mean, math.sqrt(variance / n)",
        "return mean, math.sqrt(sum((v - mean) ** 2 for v in values) / n / n)",
        "Standard error uses divisor n instead of n-1; the printed se at four decimals must change.",
    ),
    "m5-L03-exact-sum-off-by-one-step": (
        "L03",
        "return sum(((b * b - a * a) ** 2 for a, b in pairwise(points)), Fraction(0))",
        "return sum(((b * b - a * a) ** 2 for a, b in pairwise(points[1:])), Fraction(0))",
        "Exact t-squared sum drops the first interval; the closed-form match must print False.",
    ),
    "m6-L01-variance-scale-wrong": (
        "L01",
        "width = t / 2**n",
        "width = t / 2**(n + 1)",
        "Dyadic piece length halved; the variance sums print half of t, not t.",
    ),
}


def run(path: str) -> tuple[int, str, str]:
    with tempfile.TemporaryDirectory(prefix="sc1lab") as d:
        proc = subprocess.run(
            [sys.executable, "-I", "-W", "error", path],
            cwd=d,
            capture_output=True,
            text=True,
            timeout=120,
        )
    return proc.returncode, proc.stdout, proc.stderr


def expected_block(unit: str) -> str:
    text = open(PAGES[unit], encoding="utf-8").read()
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    assert m, unit
    return html.unescape(m.group(1))


def main() -> int:
    os.makedirs(MUT_DIR, exist_ok=True)
    ok = True
    for unit in PAGES:
        rc, out, err = run(TWINS[unit])
        same = out.strip() == expected_block(unit).strip()
        print(f"baseline {unit}: rc={rc} stderr_bytes={len(err)} matches_expected={same}")
        ok = ok and rc == 0 and same and not err
    for name, (unit, old, new, desc) in MUTANTS.items():
        src = open(TWINS[unit], encoding="utf-8").read()
        count = src.count(old)
        assert count == 1, (name, count)
        mutated = src.replace(old, new)
        path = os.path.join(MUT_DIR, f"{name}.py")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(f"# MUTANT {name}: {desc}\n" + mutated)
        rc, out, err = run(path)
        same = out.strip() == expected_block(unit).strip()
        status = "SURVIVED" if (rc == 0 and same) else "KILLED"
        first = ""
        if status == "KILLED":
            exp_lines = expected_block(unit).strip().splitlines()
            out_lines = out.strip().splitlines()
            for a, b in zip(exp_lines, out_lines):
                if a != b:
                    first = f" first diff: expected {a!r} got {b!r}"
                    break
            else:
                first = f" line counts expected {len(exp_lines)} got {len(out_lines)}, rc={rc}"
        print(f"{name} {status} rc={rc}{first}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
