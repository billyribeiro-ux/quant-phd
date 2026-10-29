"""Writes three new student-error mutants of the M6 reference into ledgers/M6/mutants/ (round 5).

Each mutant is the reference module with exactly one line changed; the changed line is marked.
Run from the checkout root: python3 -I ledgers/M6/scripts/M6-d-r5/make_mutants_r5.py
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
REF = ROOT / "course/modules/M/M6/grader/reference.py"
OUT = ROOT / "ledgers/M6/mutants"

MUTANTS = {
    "r5_01_dyadic_value_at_one_leaves_cell_range.py": (
        "The dyadic value at x = 1 is computed from an index one past the last cell, so it is the midpoint of a cell "
        "that does not exist.",
        "    index = min(int(point * cells), cells - 1)  # point is in [0, 1], so truncation is the floor",
        "    index = int(point * cells)  # MUTANT: the single change",
    ),
    "r5_02_stop_cap_takes_one_step_too_few.py": (
        "The stopping rule is checked for one step fewer than its cap, so every path is stopped one step early.",
        "    for _ in range(cap):",
        "    for _ in range(cap - 1):  # MUTANT: the single change",
    ),
    "r5_03_doob_threshold_strict_not_reached.py": (
        "Doob's event uses a strict threshold, so a path that reaches the level exactly is not counted as reaching it.",
        "                key = (new_position, reached or abs(new_position) >= lam)",
        "                key = (new_position, reached or abs(new_position) > lam)  # MUTANT: the single change",
    ),
}


def main() -> None:
    source = REF.read_text(encoding="utf-8")
    for name, (description, old, new) in MUTANTS.items():
        if source.count(old) != 1:
            raise SystemExit(f"{name}: anchor found {source.count(old)} times, expected 1")
        body = source.replace(old, new)
        header = f'"""{description}\n\nBased on the reference solution; the single change is marked in the code.\n"""'
        # Replace the reference module docstring (first triple-quoted block) with the mutant header.
        end = body.index('"""', 3) + 3
        body = header + body[end:]
        (OUT / name).write_text(body, encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
