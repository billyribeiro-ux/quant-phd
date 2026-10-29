"""Write the round-7 student-error mutants of the E2 engine from the reference solution (verifier-authored).

Each mutant replaces the module's first docstring line with a one-line description of the error, then applies one edit.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/E/E2/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/E2/mutants"
FIRST_LINE = REF.splitlines()[0]

MUTANTS: dict[str, tuple[str, str, str]] = {
    "r7_01_efficiency_takes_first_units_as_winners.py": (
        "Student error: efficiency takes the first `units` bidders as the winners, so the bids are ignored.",
        "    won = sum(values[i] for i, winner in enumerate(allocate(bids, units)) if winner)",
        "    won = sum(values[:units])",
    ),
    "r7_02_allocate_repeats_the_max_index.py": (
        "Student error: allocate finds each winner as the first index of the highest bid and never removes it.",
        "    winners = set(_ranking(bids)[:units])\n    return [i in winners for i in range(len(bids))]",
        "    flags = [False] * len(bids)\n    for _ in range(units):\n        flags[bids.index(max(bids))] = True\n    return flags",
    ),
    "r7_03_revenue_ignores_the_format.py": (
        "Student error: revenue always applies the uniform rule, so the format argument is ignored.",
        "    return sum(payments(format, bids, units))",
        '    return sum(payments("uniform", bids, units))',
    ),
    "r7_04_zero_cents_refused.py": (
        "Student error: zero is treated as an invalid amount, so a zero bid or value is refused.",
        "        if isinstance(amount, bool) or not isinstance(amount, int) or amount < 0:",
        "        if isinstance(amount, bool) or not isinstance(amount, int) or amount <= 0:",
    ),
}

for name, (description, old, new) in MUTANTS.items():
    if old not in REF:
        raise SystemExit(f"{name}: anchor not found")
    text = REF.replace(FIRST_LINE, '"""' + description, 1).replace(old, new, 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
