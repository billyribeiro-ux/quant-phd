"""Run new student-error mutants (m9*) and valid alternative implementations (alt9*) of the two lab twins.

Usage: python -I mutants_r9.py <checkout> <scratch_dir>
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
    ("m9a-L07-no-remainder-last-year", "L07",
     "        return grant.value_cents - base * (grant.vest_years - 1)\n", "        return base\n", "FAIL"),
    ("m9b-L07-vest-off-by-one", "L07",
     "    if index < 0 or index >= grant.vest_years:\n", "    if index < 0 or index > grant.vest_years:\n", "FAIL"),
    ("m9c-L07-apic-sign", "L07",
     "        apic_change = expense\n", "        apic_change = -expense\n", "FAIL"),
    ("m9d-L07-cfo-without-addback", "L07",
     "        cfo = net_income + expense\n", "        cfo = net_income\n", "FAIL"),
    ("alt9a-L07-round-half-up-base", "L07",
     "    base = grant.value_cents // grant.vest_years\n",
     "    base = (grant.value_cents + grant.vest_years // 2) // grant.vest_years\n", "PASS"),
    ("alt9b-L07-remainder-in-first-year", "L07",
     "    if index == grant.vest_years - 1:\n        return grant.value_cents - base * (grant.vest_years - 1)\n    return base\n",
     "    if index == 0:\n        return grant.value_cents - base * (grant.vest_years - 1)\n    return base\n", "PASS"),
    ("m9e-L08-current-tax-ignores-difference", "L08",
     "        current = RATE_PERCENT * taxable // 100\n", "        current = RATE_PERCENT * pretax[index] // 100\n", "FAIL"),
    ("m9f-L08-dtl-sign-flipped", "L08",
     "        dtl = RATE_PERCENT * cumulative // 100\n", "        dtl = -RATE_PERCENT * cumulative // 100\n", "FAIL"),
    ("m9g-L08-dtl-without-rate", "L08",
     "        dtl = RATE_PERCENT * cumulative // 100\n", "        dtl = cumulative\n", "FAIL"),
    ("alt9c-L08-deferred-from-difference", "L08",
     "        deferred = dtl - previous_dtl\n", "        deferred = RATE_PERCENT * difference // 100\n", "PASS"),
]
src = {"L07": L07, "L08": L08}
name = {"L07": "lab-AC1-L07-1.py", "L08": "lab-AC1-L08-1.py"}
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
