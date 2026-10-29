"""Verifier round 3 (E2-d): writes four new student-error mutants from the reference solution, one edit each.

Usage (repository root): .venv/bin/python -I ledgers/E2/scripts/E2-d-r3/make_mutants_r3.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/E/E2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E2/mutants"

# (file name, first docstring line, old text, new text); each old text occurs exactly once in reference.py
MUTANTS = [
    (
        "n01_efficiency_best_uses_units_minus_one.py",
        "efficiency: the best attainable uses the units-1 highest values, one value short of the units highest.",
        "best = sum(sorted(values, reverse=True)[:units])",
        "best = sum(sorted(values, reverse=True)[: units - 1])",
    ),
    (
        "n02_uniform_clearing_by_index_not_rank.py",
        "uniform price: the clearing bid is the bid of bidder number `units` by index, not the ranked bid.",
        "clearing = bids[order[units]]",
        "clearing = bids[units]",
    ),
    (
        "n03_uniform_symmetric_bid_shaded.py",
        "symmetric bid: the uniform format also shades the value by (n-1)/n, copying the first-price formula.",
        '    if format == "uniform":\n        return value\n',
        '    if format == "uniform":\n        return (n - 1) * value // n\n',
    ),
    (
        "n04_uniform_losers_pay_clearing.py",
        "payments: under the uniform format every bidder, winner or loser, is charged the clearing price.",
        "    result = [0] * len(bids)\n    for i in order[:units]:\n        result[i] = clearing if format == \"uniform\" else bids[i]\n    return result",
        "    result = [0] * len(bids)\n    if format == \"uniform\":\n        return [clearing] * len(bids)\n    for i in order[:units]:\n        result[i] = bids[i]\n    return result",
    ),
]

for name, doc, old, new in MUTANTS:
    assert REF.count(old) == 1, (name, REF.count(old))
    head, _, body = REF.partition('"""')
    _, _, rest = body.partition('"""')  # drop the module docstring
    text = f'"""{doc}\n\nGenerated from grader/reference.py by make_mutants_r3.py: one edit.\n"""' + rest
    text = text.replace(old, new, 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
