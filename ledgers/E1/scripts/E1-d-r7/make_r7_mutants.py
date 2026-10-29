"""Writes the round-7 verifier mutants (r7v_*) from the reference solution by one textual change each.

Each mutant is a complete market_structure module; its docstring's first line describes the student error.
"""

from __future__ import annotations

import sys
from pathlib import Path

REF = Path(sys.argv[1]) / "course/modules/E/E1/grader/reference.py"
OUT = Path(sys.argv[1]) / "ledgers/E1/mutants"
ref = REF.read_text(encoding="utf-8")

MUTANTS: dict[str, tuple[str, str, str]] = {
    # name: (description, old, new)
    "r7v_m01_float_division_everywhere": (
        "Student uses float true division for every exact quotient, then rounds the float once.",
        "    d = Fraction(a - b * c)\n    if structure == \"monopoly\":\n        volume = d / 2\n        fee = Fraction(a + b * c, 2 * b)\n    elif structure == \"cournot\":\n        volume = 2 * d / 3\n        fee = Fraction(a + 2 * b * c, 3 * b)\n    else:\n        volume = d\n        fee = Fraction(c)",
        "    d = a - b * c\n    if structure == \"monopoly\":\n        volume = d / 2\n        fee = (a + b * c) / (2 * b)\n    elif structure == \"cournot\":\n        volume = 2 * d / 3\n        fee = (a + 2 * b * c) / (3 * b)\n    else:\n        volume = d\n        fee = c",
    ),
    "r7v_m02_deadweight_not_squared": (
        "Student writes the deadweight loss as the linear gap (d - Q)/(2b), dropping the square of the triangle.",
        "    deadweight = (d - volume) ** 2 / (2 * b)",
        "    deadweight = (d - volume) / (2 * b)",
    ),
    "r7v_m03_welfare_minus_profit": (
        "Student subtracts exchange profit from consumer surplus for welfare, a sign error on the profit term.",
        "    welfare = consumer + profit",
        "    welfare = consumer - profit",
    ),
    "r7v_m04_bertrand_profit_forgets_cost": (
        "Student takes Bertrand profit as fee times volume, forgetting the cost of one trade.",
        "    profit = (fee - c) * volume",
        "    profit = (fee if structure == \"bertrand\" else fee - c) * volume",
    ),
    "r7v_m05_cournot_fee_monopoly_formula": (
        "Student copies the monopoly fee (a + bc)/(2b) into the Cournot branch instead of (a + 2bc)/(3b).",
        "        fee = Fraction(a + 2 * b * c, 3 * b)",
        "        fee = Fraction(a + b * c, 2 * b)",
    ),
}

OUT.mkdir(parents=True, exist_ok=True)
for name, (description, old, new) in MUTANTS.items():
    if ref.count(old) != 1:
        raise SystemExit(f"{name}: anchor found {ref.count(old)} times")
    body = ref.replace(old, new, 1)
    body = body.replace('"""Reference solution for the E1 project: market_structure.py, the trade-fee engine of the specification.',
                        f'"""{description}', 1)
    (OUT / f"{name}.py").write_text(body, encoding="utf-8")
    print("wrote", name)
