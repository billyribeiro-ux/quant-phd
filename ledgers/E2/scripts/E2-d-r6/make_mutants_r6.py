"""Write the four round-6 student-error mutants of the E2 grader into ledgers/E2/mutants/.

Run from the repository root: .venv/bin/python ledgers/E2/scripts/E2-d-r6/make_mutants_r6.py
Each mutant is course/modules/E/E2/grader/reference.py with one edit, under a one-line docstring that names the error.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path.cwd()
SRC = (ROOT / "course/modules/E/E2/grader/reference.py").read_text(encoding="utf-8")
HEAD = '"""Reference solution'
SPECS = {
    "r6_01_efficiency_skips_unit_check.py": (
        "Student error: efficiency does not check the unit count and sums the values of the first `units` ranked "
        "bidders directly, so units above the bidder count returns a pair instead of a ValueError.",
        "    _check_units(len(bids), units)\n    won = sum(values[i] for i, winner in enumerate(allocate(bids, units)) if winner)",
        "    won = sum(values[i] for i in _ranking(bids)[:units])",
    ),
    "r6_02_allocate_strict_threshold.py": (
        "Student error: allocate awards only the bids strictly above the clearing bid, so a tie at the cut-off wins nothing.",
        "    winners = set(_ranking(bids)[:units])\n    return [i in winners for i in range(len(bids))]",
        "    clearing = sorted(bids, reverse=True)[units]\n    return [bids[i] > clearing for i in range(len(bids))]",
    ),
    "r6_03_uniform_bid_unchecked_negative_value.py": (
        "Student error: the uniform symmetric bid returns a negative value unchanged, because the sign check is applied to the first-price branch only.",
        '    _check_cents("value", [value])\n    if format == "uniform":\n        return value',
        '    if format == "uniform":\n        return value\n    _check_cents("value", [value])',
    ),
    "r6_04_allocate_includes_clearing_ties.py": (
        "Student error: allocate awards every bidder whose bid equals or exceeds the clearing bid, so a tie at the cut-off wins too.",
        "    winners = set(_ranking(bids)[:units])\n    return [i in winners for i in range(len(bids))]",
        "    clearing = sorted(bids, reverse=True)[units - 1]\n    return [bids[i] >= clearing for i in range(len(bids))]",
    ),
}

for name, (doc, old, new) in SPECS.items():
    assert SRC.count(old) == 1, name
    assert SRC.count(HEAD) == 1
    body = SRC.replace(old, new).replace(HEAD, '"""' + doc + "\n\nReference solution", 1)
    (ROOT / "ledgers/E2/mutants" / name).write_text(body, encoding="utf-8")
    print("wrote", name)
