"""Round 23 (AC1-c): three NEW student-error mutants and three alternative correct implementations
of the lab twins (L07 and L08). Usage: python -I mutants_r23_new.py <checkout> <scratch_dir>
A mutant with expected FAIL must exit non-zero. An alternative with expected PASS must exit 0.
A mutant with expected PASS that exits 0 is a lab survivor, classified in the fragment.
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
L07_TAIL = "    base = grant.value_cents // grant.vest_years\n    if index == grant.vest_years - 1:\n        return grant.value_cents - base * (grant.vest_years - 1)\n    return base\n"
cases = [
    (
        "m23a-L07-last-year-remainder-one-base-short",
        "L07",
        "        return grant.value_cents - base * (grant.vest_years - 1)\n",
        "        return grant.value_cents - base * (grant.vest_years - 2)\n",
        "FAIL",
    ),
    (
        "m23b-L08-book-depreciation-on-carrying-amount",
        "L08",
        "        book_dep = cost // LIFE\n",
        "        book_dep = (cost - book_total) * 20 // 100\n",
        "FAIL",
    ),
    (
        "m23c-L07-base-divides-by-horizon",
        "L07",
        "    base = grant.value_cents // grant.vest_years\n",
        "    base = grant.value_cents // HORIZON\n",
        "PASS",
    ),
    (
        "alt23a-L07-remainder-cents-spread-over-first-years",
        "L07",
        L07_TAIL,
        "    q, r = divmod(grant.value_cents, grant.vest_years)\n    return q + 1 if index < r else q\n",
        "PASS",
    ),
    (
        "alt23b-L08-cumulative-from-running-totals",
        "L08",
        "        cumulative += difference\n",
        "        cumulative = tax_total + tax_dep - (book_total + book_dep)\n",
        "PASS",
    ),
    (
        "alt23c-L08-current-tax-round-half-up-cutoff",
        "L08",
        "        current = RATE_PERCENT * taxable // 100\n",
        "        current = (RATE_PERCENT * taxable + 50) // 100\n",
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
