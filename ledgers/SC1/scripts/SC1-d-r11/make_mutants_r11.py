#!/usr/bin/env python3
"""Write the round-11 student-error mutants of the SC1 project reference into ledgers/SC1/mutants/.

Each mutant is the reference solution (course/modules/SC/SC1/grader/reference.py) with exactly one edit, applied
by exact string replacement that must match once. Run from the checkout root:
    .venv/bin/python ledgers/SC1/scripts/SC1-d-r11/make_mutants_r11.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REFERENCE = ROOT / "course/modules/SC/SC1/grader/reference.py"
OUT = ROOT / "ledgers/SC1/mutants"

MUTANTS: dict[str, tuple[str, str, str]] = {
    "r11_01_coarse_grid_ends_one_step_early.py": (
        '"""Coarse grid ends one step early: nested_grid_counts drops the horizon point t_H from the coarse grid, so the\n'
        "coarse maximum is taken over the coarse points before the last one.\n\n"
        'Single-change copy of the reference (round 11, verifier-written)."""',
        "coarse = sum(1 for values in paths if max(values[stride - 1 :: stride]) >= level)",
        "coarse = sum(1 for values in paths if max(values[stride - 1 : n_fine - 1 : stride] or [-math.inf]) >= level)",
    ),
    "r11_02_reflection_tail_rounded_inside.py": (
        '"""Rounding inside the engine: reflection_tail rounds its closed form to six decimal places before returning, as\n'
        "if the printing rule belonged to the function.\n\n"
        'Single-change copy of the reference (round 11, verifier-written)."""',
        "    return math.erfc(a / math.sqrt(2.0 * t))",
        "    return round(math.erfc(a / math.sqrt(2.0 * t)), 6)",
    ),
    "r11_03_coarse_count_strict_inequality.py": (
        '"""Strict inequality on the coarse grid only: nested_grid_counts counts a path on the coarse grid only when its\n'
        "coarse maximum is strictly above a, so a coarse maximum equal to the level is dropped.\n\n"
        'Single-change copy of the reference (round 11, verifier-written)."""',
        "coarse = sum(1 for values in paths if max(values[stride - 1 :: stride]) >= level)",
        "coarse = sum(1 for values in paths if max(values[stride - 1 :: stride]) > level)",
    ),
    "r11_04_grid_draws_reseeded_per_grid_size.py": (
        '"""Seed shifted by the grid size: _grid_paths seeds the Gaussian draws with the instance seed plus n_steps, so each\n'
        "grid size draws from its own stream instead of the instance's stream.\n\n"
        'Single-change copy of the reference (round 11, verifier-written)."""',
        "    rng = random.Random(int(instance[\"seed\"]))\n    sd = math.sqrt(float(instance[\"H\"]) / n_steps)",
        "    rng = random.Random(int(instance[\"seed\"]) + n_steps)\n    sd = math.sqrt(float(instance[\"H\"]) / n_steps)",
    ),
}


def main() -> None:
    source = REFERENCE.read_text(encoding="utf-8")
    for name, (docstring_head, old, new) in MUTANTS.items():
        # The header replaces the reference's module docstring; the body is the reference with one edit.
        count = source.count(old)
        if count != 1:
            raise SystemExit(f"{name}: expected one match of the edit, found {count}")
        body = source.replace(old, new, 1)
        head_end = body.index('"""', body.index('"""') + 3) + 3  # end of the module docstring
        text = docstring_head + body[head_end:]
        (OUT / name).write_text(text, encoding="utf-8")
        print(f"wrote {name}")


if __name__ == "__main__":
    main()
