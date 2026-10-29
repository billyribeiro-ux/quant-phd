"""Round 18 (AC1-c): re-runs every archived lab mutant (r7, r8, r9, r10, r17), the round-18 new
student-error mutants (m18*) and alternative correct implementations (alt18*) of the two lab twins.

Usage: python -I mutants_r18.py <checkout> <scratch_dir>
Each case: (id, lab, old, new, expected). A mutant with expected FAIL must exit non-zero; an
alternative with expected PASS must exit 0. Survivors are printed with their printed-table diff
(the first differing output line) so the page statements can be checked against them.
"""

import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
L07 = (root / "tests/labs/AC1/lab-AC1-L07-1.py").read_text(encoding="utf-8")
L08 = (root / "tests/labs/AC1/lab-AC1-L08-1.py").read_text(encoding="utf-8")
SBC = "    sbc = [sum(yearly_expense(g, year) for g in grants) for year in range(1, HORIZON + 1)]\n"
BASE = "    base = grant.value_cents // grant.vest_years\n"
cases = [
    # r7
    (
        "r7-m8a-L08-deferred-from-taxable",
        "L08",
        "        deferred = dtl - previous_dtl\n",
        "        deferred = RATE_PERCENT * taxable // 100\n",
        "FAIL",
    ),
    (
        "r7-m7a-L07-last-year-branch-disabled",
        "L07",
        "    if index == grant.vest_years - 1:\n",
        "    if False:\n",
        "FAIL",
    ),
    ("r7-m7b-L07-base-plus-one-cent", "L07", "    return base\n", "    return base + 1\n", "FAIL"),
    # r8
    ("r8-n1ceil-L07-ceiling-base", "L07", BASE, "    base = -(-grant.value_cents // grant.vest_years)\n", "PASS?"),
    (
        "r8-n1b-L07-ceil-by-addition",
        "L07",
        BASE,
        "    base = grant.value_cents // grant.vest_years + (1 if grant.value_cents % grant.vest_years else 0)\n",
        "PASS?",
    ),
    (
        "r8-n2life-L08-book-life-minus-one",
        "L08",
        "        book_dep = cost // LIFE\n",
        "        book_dep = cost // (LIFE - 1)\n",
        "FAIL",
    ),
    (
        "r8-n3sign-L08-deferred-sign",
        "L08",
        "        deferred = dtl - previous_dtl\n",
        "        deferred = previous_dtl - dtl\n",
        "FAIL",
    ),
    (
        "r8-n4te-L08-total-omits-deferred",
        "L08",
        "        tax_expense = current + deferred\n",
        "        tax_expense = current\n",
        "FAIL",
    ),
    # r9
    (
        "m9a-L07-no-remainder-last-year",
        "L07",
        "        return grant.value_cents - base * (grant.vest_years - 1)\n",
        "        return base\n",
        "FAIL",
    ),
    (
        "m9b-L07-vest-off-by-one",
        "L07",
        "    if index < 0 or index >= grant.vest_years:\n",
        "    if index < 0 or index > grant.vest_years:\n",
        "FAIL",
    ),
    ("m9c-L07-apic-sign", "L07", "        apic_change = expense\n", "        apic_change = -expense\n", "FAIL"),
    (
        "m9d-L07-cfo-without-addback",
        "L07",
        "        cfo = net_income + expense\n",
        "        cfo = net_income\n",
        "FAIL",
    ),
    (
        "m9e-L08-current-tax-ignores-difference",
        "L08",
        "        current = RATE_PERCENT * taxable // 100\n",
        "        current = RATE_PERCENT * pretax[index] // 100\n",
        "FAIL",
    ),
    (
        "m9f-L08-dtl-sign-flipped",
        "L08",
        "        dtl = RATE_PERCENT * cumulative // 100\n",
        "        dtl = -RATE_PERCENT * cumulative // 100\n",
        "FAIL",
    ),
    (
        "m9g-L08-dtl-without-rate",
        "L08",
        "        dtl = RATE_PERCENT * cumulative // 100\n",
        "        dtl = cumulative\n",
        "FAIL",
    ),
    (
        "alt9a-L07-round-half-up-base",
        "L07",
        BASE,
        "    base = (grant.value_cents + grant.vest_years // 2) // grant.vest_years\n",
        "PASS",
    ),
    (
        "alt9b-L07-remainder-in-first-year",
        "L07",
        "    if index == grant.vest_years - 1:\n        return grant.value_cents - base * (grant.vest_years - 1)\n    return base\n",
        "    if index == 0:\n        return grant.value_cents - base * (grant.vest_years - 1)\n    return base\n",
        "PASS",
    ),
    (
        "alt9c-L08-deferred-from-difference",
        "L08",
        "        deferred = dtl - previous_dtl\n",
        "        deferred = RATE_PERCENT * difference // 100\n",
        "PASS",
    ),
    # r10
    (
        "m10a-L07-expense-starts-one-year-late",
        "L07",
        "    index = year - grant.grant_year\n",
        "    index = year - grant.grant_year - 1\n",
        "PASS?",
    ),
    (
        "m10b-L07-apic-change-one-cent-short",
        "L07",
        "        apic_change = expense\n",
        "        apic_change = expense - 1\n",
        "FAIL",
    ),
    (
        "m10c-L07-base-divides-by-vest-plus-one",
        "L07",
        BASE,
        "    base = grant.value_cents // (grant.vest_years + 1)\n",
        "PASS?",
    ),
    (
        "m10d-L08-deferred-expense-is-balance",
        "L08",
        "        deferred = dtl - previous_dtl\n",
        "        deferred = dtl\n",
        "FAIL",
    ),
    (
        "m10e-L08-current-tax-adds-difference",
        "L08",
        "        current = RATE_PERCENT * taxable // 100\n",
        "        current = RATE_PERCENT * (pretax[index] + difference) // 100\n",
        "FAIL",
    ),
    (
        "alt10a-L07-ceil-base-remainder-last",
        "L07",
        BASE,
        "    base = -(-grant.value_cents // grant.vest_years)\n",
        "PASS",
    ),
    (
        "alt10b-L08-deferred-rate-times-difference",
        "L08",
        "        deferred = dtl - previous_dtl\n",
        "        deferred = RATE_PERCENT * difference // 100\n",
        "PASS",
    ),
    # r17
    (
        "m17a-L07-sbc-row-starts-at-year-zero",
        "L07",
        SBC,
        "    sbc = [sum(yearly_expense(g, year) for g in grants) for year in range(0, HORIZON)]\n",
        "FAIL",
    ),
    (
        "m17b-L07-vesting-window-one-year-long",
        "L07",
        "    if index < 0 or index >= grant.vest_years:\n",
        "    if index < 0 or index > grant.vest_years:\n",
        "FAIL",
    ),
    (
        "m17c-L07-last-year-takes-base",
        "L07",
        "        return grant.value_cents - base * (grant.vest_years - 1)\n",
        "        return base\n",
        "FAIL",
    ),
    (
        "m17d-L08-tax-depreciation-first-percent-every-year",
        "L08",
        "        tax_dep = cost * TAX_PERCENT[index] // 100\n",
        "        tax_dep = cost * TAX_PERCENT[0] // 100\n",
        "FAIL",
    ),
    (
        "m17e-L08-cumulative-not-accumulated",
        "L08",
        "        cumulative += difference\n",
        "        cumulative = difference\n",
        "FAIL",
    ),
    (
        "alt17a-L08-current-tax-from-pretax-minus-difference",
        "L08",
        "        current = RATE_PERCENT * taxable // 100\n",
        "        current = (RATE_PERCENT * pretax[index] - RATE_PERCENT * difference) // 100\n",
        "PASS",
    ),
    # r18 new student-error mutants
    (
        "m18a-L07-schedule-check-skips-last-year",
        "L07",
        "    for grant in grants:\n        expensed = sum(yearly_expense(grant, year) for year in range(1, HORIZON + 1))\n",
        "    for grant in grants:\n        expensed = sum(yearly_expense(grant, year) for year in range(1, HORIZON))\n",
        "FAIL",
    ),
    (
        "m18b-L07-cash-change-equals-apic",
        "L07",
        "        cash_change = cfo\n",
        "        cash_change = apic_change\n",
        "FAIL",
    ),
    (
        "m18c-L07-sbc-omits-last-grant",
        "L07",
        SBC,
        "    sbc = [sum(yearly_expense(g, year) for g in grants[:-1]) for year in range(1, HORIZON + 1)]\n",
        "PASS?",
    ),
    (
        "m18d-L08-tax-depreciation-shifted-one-year",
        "L08",
        "        tax_dep = cost * TAX_PERCENT[index] // 100\n",
        "        tax_dep = cost * TAX_PERCENT[index - 1] // 100\n",
        "FAIL",
    ),
    ("m18e-L08-deferred-uses-stale-balance", "L08", "        previous_dtl = dtl\n", "        pass\n", "FAIL"),
    (
        "m18f-L08-total-expense-uses-balance",
        "L08",
        "        tax_expense = current + deferred\n",
        "        tax_expense = current + dtl\n",
        "FAIL",
    ),
    (
        "m18g-L07-base-floor-of-share-count",
        "L07",
        BASE,
        "    base = grant.shares // grant.vest_years * grant.fair_value_cents\n",
        "FAIL",
    ),
    # r18 alternative correct implementations (different algorithms / numerical cutoffs)
    (
        "alt18a-L07-cumulative-rounding-schedule",
        "L07",
        "    base = grant.value_cents // grant.vest_years\n    if index == grant.vest_years - 1:\n"
        "        return grant.value_cents - base * (grant.vest_years - 1)\n    return base\n",
        "    return grant.value_cents * (index + 1) // grant.vest_years - grant.value_cents * index // grant.vest_years\n",
        "PASS",
    ),
    (
        "alt18b-L08-dtl-by-accumulated-rate-steps",
        "L08",
        "        dtl = RATE_PERCENT * cumulative // 100\n",
        "        dtl = previous_dtl + RATE_PERCENT * difference // 100\n",
        "PASS",
    ),
    (
        "alt18c-L08-tax-expense-from-rate-times-pretax",
        "L08",
        "        tax_expense = current + deferred\n",
        "        tax_expense = RATE_PERCENT * pretax[index] // 100\n",
        "PASS",
    ),
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
    print(f"{case}: exit={proc.returncode} observed={outcome} expected={expect} | {last[:100]}")
