"""Writes the verifier's round-3 student-error mutants of the FC1 reference into ledgers/FC1/mutants/.

Usage: python ledgers/FC1/scripts/FC1-c-r3/make_mutants_r3.py <checkout-root>
Each mutant is reference.py with one exact string replaced; the script asserts that each replacement matched once.
"""

from __future__ import annotations

import sys
from pathlib import Path

root = Path(sys.argv[1])
ref = (root / "course/modules/FC/FC1/grader/reference.py").read_text(encoding="utf-8")

MUTANTS: dict[str, list[tuple[str, str]]] = {
    "c3n01_face_capped_at_five_million.py": [
        (
            '        if face <= 0:\n            raise ValueError("face_cents must be positive")\n',
            '        if face <= 0:\n            raise ValueError("face_cents must be positive")\n'
            "        if face > 5_000_000:\n"
            '            raise ValueError("face_cents above 5,000,000 is not supported")\n',
        ),
    ],
    "c3n02_settlement_capped_at_five_periods.py": [
        (
            '        if day < 1:\n            raise ValueError("settlement_day must be at least 1")\n',
            '        if day < 1 or day > 5:\n            raise ValueError("settlement_day must be between 1 and 5")\n',
        ),
    ],
    "c3n03_price_discounts_one_period_short.py": [
        ("        total += Fraction(amount) / (1 + y) ** period\n", "        total += Fraction(amount) / (1 + y) ** (period - 1)\n"),
    ],
    "c3n04_warns_on_negative_yield.py": [
        (
            "    y = Fraction(rate, 10_000)\n    total = Fraction(0)\n",
            "    y = Fraction(rate, 10_000)\n    if rate < 0:\n"
            "        import warnings\n\n        warnings.warn('negative yield', UserWarning)\n"
            "    total = Fraction(0)\n",
        ),
    ],
    "c3n05_yield_read_as_percent.py": [
        ("    y = Fraction(rate, 10_000)\n", "    y = Fraction(rate, 100)\n"),
    ],
}

HEADERS = {
    "c3n01_face_capped_at_five_million.py": "Bond refuses face_cents above 5,000,000, a cap the page never states.",
    "c3n02_settlement_capped_at_five_periods.py": "CashTrade refuses settlement_day above 5, a cap the page never states.",
    "c3n03_price_discounts_one_period_short.py": "bond_price_cents discounts each event by (1 + y) ** (t - 1), one period short.",
    "c3n04_warns_on_negative_yield.py": "bond_price_cents warns (a UserWarning) at a negative yield, a valid input.",
    "c3n05_yield_read_as_percent.py": "bond_price_cents reads yield_bps as a percentage, so the per-period yield is 100 times too large.",
}

for name, reps in MUTANTS.items():
    text = ref
    for old, new in reps:
        assert text.count(old) == 1, f"{name}: replacement target not unique: {old[:50]!r}"
        text = text.replace(old, new)
    body = text.split('"""', 2)
    assert len(body) == 3, f"{name}: reference docstring not found"
    doc = f'"""{HEADERS[name]}\n\nRound-3 student-error mutant of reference.py, written by the FC1 slice-c verifier."""'
    text = doc + body[2]
    (root / "ledgers/FC1/mutants" / name).write_text(text, encoding="utf-8")
    print("wrote", name)
