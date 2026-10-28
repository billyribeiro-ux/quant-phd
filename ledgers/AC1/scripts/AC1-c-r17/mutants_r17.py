"""Round 17 (AC1-c): new student-error mutants (m17*) and alternative correct implementations (alt17*)
of the two lab twins. Usage: python -I mutants_r17.py <checkout> <scratch_dir>.
A mutant must FAIL (non-zero exit) unless it is recorded as a survivor; an alternative must PASS (exit 0).
"""

import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
L07 = (root / "tests/labs/AC1/lab-AC1-L07-1.py").read_text(encoding="utf-8")
L08 = (root / "tests/labs/AC1/lab-AC1-L08-1.py").read_text(encoding="utf-8")
cases = [
    ("m17a-L07-sbc-row-starts-at-year-zero", "L07",
     "    sbc = [sum(yearly_expense(g, year) for g in grants) for year in range(1, HORIZON + 1)]\n",
     "    sbc = [sum(yearly_expense(g, year) for g in grants) for year in range(0, HORIZON)]\n", "FAIL"),
    ("m17b-L07-vesting-window-one-year-long", "L07",
     "    if index < 0 or index >= grant.vest_years:\n",
     "    if index < 0 or index > grant.vest_years:\n", "FAIL"),
    ("m17c-L07-last-year-takes-base", "L07",
     "        return grant.value_cents - base * (grant.vest_years - 1)\n",
     "        return base\n", "FAIL"),
    ("m17d-L08-tax-depreciation-first-percent-every-year", "L08",
     "        tax_dep = cost * TAX_PERCENT[index] // 100\n",
     "        tax_dep = cost * TAX_PERCENT[0] // 100\n", "FAIL"),
    ("m17e-L08-cumulative-not-accumulated", "L08",
     "        cumulative += difference\n", "        cumulative = difference\n", "FAIL"),
    ("alt17a-L08-current-tax-from-pretax-minus-difference", "L08",
     "        current = RATE_PERCENT * taxable // 100\n",
     "        current = (RATE_PERCENT * pretax[index] - RATE_PERCENT * difference) // 100\n", "PASS"),
]
src = {"L07": L07, "L08": L08}
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
    verdict = "as expected" if outcome == expect else "UNEXPECTED"
    print(f"{case}: exit={proc.returncode} observed={outcome} expected={expect} {verdict} | {last[:110]}")
