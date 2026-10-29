"""Writes the round-2 student-error mutants of the E1 project grader into ledgers/E1/mutants/.

Each mutant is a complete module derived from course/modules/E/E1/grader/reference.py by one textual edit; the
edit is asserted to match exactly once so that no mutant is silently identical to the reference.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REF = (ROOT / "course/modules/E/E1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E1/mutants"

CHECKS_OLD = '''    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
'''

MUTANTS = {
    "r2_m01_b_check_only_in_monopoly.py": (
        "The b > 0 check runs only for the monopoly; cournot and bertrand accept b <= 0 without ValueError.",
        CHECKS_OLD,
        '''    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if a <= b * c:
        raise ValueError("a must exceed b*c")
    if structure == "monopoly" and b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
''',
    ),
    "r2_m02_a_check_only_in_cournot.py": (
        "The a > b*c check runs only for cournot; monopoly and bertrand accept a <= b*c without ValueError.",
        CHECKS_OLD,
        '''    if structure not in STRUCTURES:
        raise ValueError("structure must be one of monopoly, cournot, bertrand")
    if structure == "cournot" and a <= b * c:
        raise ValueError("a must exceed b*c")
    if b <= 0:
        raise ValueError("b must be positive")
    if c <= 0:
        raise ValueError("c must be positive")
''',
    ),
    "r2_m03_deadweight_gap_drops_b.py": (
        "Deadweight loss uses the gap d = a - c (the b factor dropped from the gap), so it is wrong whenever b > 1.",
        "    d = Fraction(a - b * c)\n",
        "    d = Fraction(a - c)\n",
    ),
    "r2_m04_profit_from_rounded_fee.py": (
        "Profit is (fee rounded to the cent - c) times the exact volume, so the exact fee's rounding leaks into profit.",
        "        profit = (fee - c) * volume\n",
        "        profit = (half_up(fee) - c) * volume\n",
    ),
}

# The reference profit line sits at four-space indentation in outcome(); patch by exact match below.
PROFIT_OLD = "    profit = (fee - c) * volume\n"
PROFIT_NEW = "    profit = (half_up(fee) - c) * volume\n"

for name, (doc, old, new) in MUTANTS.items():
    if name.startswith("r2_m04"):
        old, new = PROFIT_OLD, PROFIT_NEW
    if name.startswith("r2_m03"):
        old, new = "    d = Fraction(a - b * c)\n", "    d = Fraction(a - c)\n"
    count = REF.count(old)
    assert count == 1, (name, count)
    text = REF.replace(old, new, 1)
    if name.startswith("r2_m01") or name.startswith("r2_m02"):
        assert REF.count(CHECKS_OLD) == 1, name
        text = REF.replace(CHECKS_OLD, new, 1)
    header = f'"""{doc}"""\n'
    body = text.split('"""', 2)[2]
    (OUT / name).write_text(header + body, encoding="utf-8")
    print("wrote", name)
