"""Writes three new student-error mutants of the E2 reference (round 5, verifier E2-d). Run with python -I."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
REF = ROOT / "course" / "modules" / "E" / "E2" / "grader" / "reference.py"
OUT = ROOT / "ledgers" / "E2" / "mutants"

SPECS = {
    "y01_discriminatory_losers_pay_their_bid.py": (
        '"""Student error: under the discriminatory format a loser is charged its own bid, not 0."""\n',
        "    result = [0] * len(bids)\n",
        "    result = list(bids) if format == \"discriminatory\" else [0] * len(bids)\n",
    ),
    "y02_symmetric_bid_floors_the_half_cent.py": (
        '"""Student error: the symmetric bid is floored, so an exact half cent goes down instead of up."""\n',
        "    return math.floor(exact + Fraction(1, 2))\n",
        "    return math.floor(exact)\n",
    ),
    "y03_best_value_is_read_from_the_bid_ranking.py": (
        '"""Student error: the best attainable value is summed over the bid ranking, not over the sorted values."""\n',
        "    best = sum(sorted(values, reverse=True)[:units])\n",
        "    best = sum(values[i] for i in _ranking(bids)[:units])\n",
    ),
}

src = REF.read_text(encoding="utf-8")
for name, (doc, old, new) in SPECS.items():
    assert src.count(old) == 1, (name, src.count(old))
    body = src.replace(old, new, 1)
    # replace the module docstring with the mutant's own one-line description, keeping the rest of the module
    end = body.index('"""', body.index('"""') + 3) + 3
    body = doc + body[end:]
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
