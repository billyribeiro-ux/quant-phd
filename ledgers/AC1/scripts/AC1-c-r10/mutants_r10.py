"""Round 10 new student-error mutants (m10*) and alternative correct implementations (alt10*) of the two lab twins.

Usage: python -I mutants_r10.py <checkout> <scratch_dir>
A mutant must FAIL (non-zero exit); an alternative correct implementation must PASS (exit 0).
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
    ("m10a-L07-expense-starts-one-year-late", "L07",
     "    index = year - grant.grant_year\n", "    index = year - grant.grant_year - 1\n", "FAIL"),
    ("m10b-L07-apic-change-one-cent-short", "L07",
     "        apic_change = expense\n", "        apic_change = expense - 1\n", "FAIL"),
    ("m10c-L07-base-divides-by-vest-plus-one", "L07",
     "    base = grant.value_cents // grant.vest_years\n", "    base = grant.value_cents // (grant.vest_years + 1)\n", "FAIL"),
    ("m10d-L08-deferred-expense-is-balance", "L08",
     "        deferred = dtl - previous_dtl\n", "        deferred = dtl\n", "FAIL"),
    ("m10e-L08-current-tax-adds-difference", "L08",
     "        current = RATE_PERCENT * taxable // 100\n", "        current = RATE_PERCENT * (pretax[index] + difference) // 100\n", "FAIL"),
    ("alt10a-L07-ceil-base-remainder-last", "L07",
     "    base = grant.value_cents // grant.vest_years\n",
     "    base = -(-grant.value_cents // grant.vest_years)\n", "PASS"),
    ("alt10b-L08-deferred-rate-times-difference", "L08",
     "        deferred = dtl - previous_dtl\n", "        deferred = RATE_PERCENT * difference // 100\n", "PASS"),
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
