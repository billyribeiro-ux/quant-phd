"""Round 20 (AC1-c): three NEW student-error mutants and two alternative correct implementations of the lab twins.

Usage: python -I mutants_r20_new.py <checkout> <scratch_dir>
A mutant with expected FAIL must exit non-zero. An alternative with expected PASS must exit 0.
"""

import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
src = {
    "L07": (root / "tests/labs/AC1/lab-AC1-L07-1.py").read_text(encoding="utf-8"),
    "L08": (root / "tests/labs/AC1/lab-AC1-L08-1.py").read_text(encoding="utf-8"),
}
cases = [
    (
        "m20a-L08-tax-percent-wraps-to-first-year",
        "L08",
        "        tax_dep = cost * TAX_PERCENT[index] // 100\n",
        "        tax_dep = cost * TAX_PERCENT[(index + 1) % LIFE] // 100\n",
        "FAIL",
    ),
    (
        "m20b-L08-balance-floored-at-zero",
        "L08",
        "        dtl = RATE_PERCENT * cumulative // 100\n",
        "        dtl = RATE_PERCENT * max(cumulative, 0) // 100\n",
        "PASS?",
    ),
    (
        "m20c-L07-expense-index-shifted-by-one",
        "L07",
        "    index = year - grant.grant_year\n",
        "    index = year - grant.grant_year - 1\n",
        "FAIL",
    ),
    (
        "alt20a-L08-current-tax-from-exact-difference",
        "L08",
        "        current = RATE_PERCENT * taxable // 100\n",
        "        current = (RATE_PERCENT * pretax[index] - RATE_PERCENT * difference) // 100\n",
        "PASS",
    ),
    (
        "alt20b-L07-expense-by-cumulative-share",
        "L07",
        "    base = grant.value_cents // grant.vest_years\n    if index == grant.vest_years - 1:\n"
        "        return grant.value_cents - base * (grant.vest_years - 1)\n    return base\n",
        "    v = grant.vest_years\n    return grant.value_cents * (index + 1) // v - grant.value_cents * index // v\n",
        "PASS",
    ),
]
for case, lab, old, new, expect in cases:
    text = src[lab]
    if text.count(old) != 1:
        print(f"{case}: PATTERN COUNT {text.count(old)} (mutation not applied)")
        continue
    path = scratch / f"{case}.py"
    path.write_text(text.replace(old, new), encoding="utf-8")
    proc = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True)
    last = (proc.stderr.strip().splitlines() or ["-"])[-1]
    outcome = "FAIL" if proc.returncode != 0 else "PASS"
    print(f"{case}: exit={proc.returncode} observed={outcome} expected={expect} | {last[:100]}")
