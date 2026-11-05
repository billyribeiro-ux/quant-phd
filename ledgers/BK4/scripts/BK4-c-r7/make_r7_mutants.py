"""Writes the round-7 student-error mutants of the BK4 reference into ledgers/BK4/mutants/.

Each mutant is reference.py with exactly one change; every replacement must match exactly once.
Usage: make_r7_mutants.py <checkout>
"""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1])
REF = ROOT / "course/modules/BK/BK4/grader/reference.py"
OUT = ROOT / "ledgers/BK4/mutants"

MUTANTS: dict[str, tuple[str, list[tuple[str, str]]]] = {
    "s01_leftover_to_largest_fund_first.py": (
        "Student error: the leftover cents go to the largest default funds first (ties by id), not to the first survivors in ascending id order.",
        [
            (
                "        for member in survivors:\n            if leftover == 0:",
                "        for member in sorted(survivors, key=lambda m: (-default_fund_cents[m], m)):\n            if leftover == 0:",
            )
        ],
    ),
    "s02_shares_weighted_by_margins.py": (
        "Student error: the residual is shared in proportion to the survivors' initial margins, not their default funds.",
        [
            (
                "            survivor_cents[member] = residual * default_fund_cents[member] // total_fund\n        leftover = residual - sum(survivor_cents.values())",
                "            total_margin = sum(initial_margin_cents[m] for m in survivors)\n            survivor_cents[member] = residual * initial_margin_cents[member] // total_margin\n        leftover = residual - sum(survivor_cents.values())",
            )
        ],
    ),
    "s03_zero_fund_survivor_left_out.py": (
        "Student error: survivors with a zero default fund are left out of survivor_cents instead of being listed with zero.",
        [
            (
                "    return Waterfall(\n        margin_cents=margin_paid,",
                "    survivor_cents = {m: v for m, v in survivor_cents.items() if default_fund_cents[m] > 0}\n    return Waterfall(\n        margin_cents=margin_paid,",
            )
        ],
    ),
    "s04_empty_scenario_message_reworded.py": (
        "Student error: margin_for_cover refuses an empty scenario set with a message that does not say at least one scenario is needed.",
        [
            (
                '        raise ValueError("at least one scenario is needed")\n    if not 1 <= target_bps',
                '        raise ValueError("no scenarios were given")\n    if not 1 <= target_bps',
            )
        ],
    ),
    "s05_sizing_index_rounds_to_nearest.py": (
        "Student error: the sizing index rounds the exact position to the nearest whole scenario instead of rounding it up.",
        [
            (
                "    index = -((-target_bps * count) // 10_000)",
                "    index = max(1, (target_bps * count + 5_000) // 10_000)",
            )
        ],
    ),
}


def main() -> None:
    source = REF.read_text(encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (description, edits) in MUTANTS.items():
        text = source
        for old, new in edits:
            count = text.count(old)
            if count != 1:
                raise SystemExit(f"{name}: expected one match, found {count}: {old[:60]!r}")
            text = text.replace(old, new)
        header = f'"""{description}\n\nRound-7 verifier mutant of the BK4 reference (one change; see the one-line description above).\n"""\n'
        body = text.split('"""', 2)[2]  # drop the reference's own module docstring
        (OUT / name).write_text(header + body, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
