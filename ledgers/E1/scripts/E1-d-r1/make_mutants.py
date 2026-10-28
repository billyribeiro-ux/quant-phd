"""Write the verifier's student-error mutants of the E1 reference (ledgers/E1/mutants/v0N_*.py).

Each mutant is the reference solution with exactly one line changed; the script asserts that the change applied.
Run: .venv/bin/python ledgers/E1/scripts/E1-d-r1/make_mutants.py <repo-root>
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
REF = ROOT / "course/modules/E/E1/grader/reference.py"
OUT = ROOT / "ledgers/E1/mutants"

MUTANTS: dict[str, tuple[str, str, str]] = {
    "v01_consumer_surplus_missing_half": (
        "Consumer surplus Q^2/b instead of Q^2/(2b): the factor 1/2 of the area is lost.",
        "    consumer = volume * volume / (2 * b)\n",
        "    consumer = volume * volume / b\n",
    ),
    "v02_cournot_profit_one_exchange": (
        "Cournot profit reported for one exchange (half the total) instead of the two-exchange total.",
        "    profit = (fee - c) * volume\n",
        "    profit = (fee - c) * volume / (2 if structure == 'cournot' else 1)\n",
    ),
    "v03_round_half_even": (
        "Rounding by Python round() (ties to even) instead of half up.",
        "    return math.floor(x + Fraction(1, 2))\n",
        "    return round(x)\n",
    ),
    "v04_monopoly_fee_floor_division": (
        "Monopoly fee taken with integer floor division before the exact rounding step.",
        "        fee = Fraction(a + b * c, 2 * b)\n",
        "        fee = Fraction((a + b * c) // (2 * b))\n",
    ),
    "v05_b_positive_check_missing": (
        "The b > 0 check is omitted, so b <= 0 is not rejected with ValueError.",
        '    if b <= 0:\n        raise ValueError("b must be positive")\n',
        "    pass\n",
    ),
    "v06_deadweight_on_rounded_volume": (
        "Deadweight loss computed from the rounded volume, not the exact volume (the page forbids it).",
        "    deadweight = (d - volume) ** 2 / (2 * b)\n",
        "    deadweight = (d - half_up(volume)) ** 2 / (2 * b)\n",
    ),
    "v07_welfare_sum_of_rounded_parts": (
        "Welfare as the sum of the rounded consumer surplus and rounded profit, not one rounding of the exact sum.",
        "    welfare = consumer + profit\n",
        "    welfare = Fraction(half_up(consumer) + half_up(profit))\n",
    ),
    "v08_cournot_volume_integer_division": (
        "Cournot volume 2d/3 taken with integer floor division before rounding.",
        "        volume = 2 * d / 3\n",
        "        volume = Fraction((2 * d) // 3)\n",
    ),
}

for name, (description, old, new) in MUTANTS.items():
    source = REF.read_text(encoding="utf-8")
    assert source.count(old) == 1, f"{name}: the line to change was not found exactly once"
    header = f'"""MUTANT {name}: {description}\n\nWritten by the independent verifier; the reference with one line changed.\n"""\n'
    body = source.split('"""', 2)[2]  # drop the reference docstring, keep the code
    (OUT / f"{name}.py").write_text(header + body.replace(old, new), encoding="utf-8")
    print("wrote", name)
