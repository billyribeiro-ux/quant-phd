"""Write verifier round-1 student-error mutants of the M4 reference into ledgers/M4/mutants/ (verifier D, round 1).

Each mutant is the reference with exactly one substitution. A substitution must match exactly once in the reference,
or the generator stops, so no mutant can silently equal the reference. The first docstring line describes the error.
Run from the checkout root: .venv/bin/python ledgers/M4/scripts/M4-d-r1/verifyD1_make_mutants.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REFERENCE = ROOT / "course/modules/M/M4/grader/reference.py"
MUTANTS = ROOT / "ledgers/M4/mutants"

# (file stem, first docstring line, old text, new text)
SUBSTITUTIONS: list[tuple[str, str, str, str]] = [
    (
        "v1_01_losses_floored_at_zero",
        "Verifier round-1 student-error mutant. Gains are floored at zero, so a portfolio that rises records a zero loss.",
        "        losses.append(round(-total))",
        "        losses.append(max(0, round(-total)))",
    ),
    (
        "v1_02_student_t_ignores_seed",
        "Verifier round-1 student-error mutant. The Student-t family ignores the seed and draws from an unseeded generator.",
        "    rng = random.Random(seed)\n    losses: list[int] = []",
        "    rng = random.Random(seed) if family == \"gaussian\" else random.Random()\n    losses: list[int] = []",
    ),
    (
        "v1_03_quantile_index_round_half_even",
        "Verifier round-1 student-error mutant. The 99% index is round(0.99 n), not the ceiling, so n = 99 picks the 98th loss.",
        "    index = (99 * len(losses_cents) + 99) // 100",
        "    index = round(0.99 * len(losses_cents))",
    ),
    (
        "v1_04_loss_rounded_half_up_by_truncation",
        "Verifier round-1 student-error mutant. Losses are rounded by int(x + 0.5), which truncates toward zero, not to the nearest cent.",
        "        losses.append(round(-total))",
        "        losses.append(int(-total + 0.5))",
    ),
    (
        "v1_05_positions_read_in_dollars",
        "Verifier round-1 student-error mutant. Positions are read as dollars (cents divided by 100) inside the loss.",
        "            total += position_cents[i] * ret",
        "            total += position_cents[i] * ret / 100",
    ),
    (
        "v1_06_matched_factor_inverted",
        "Verifier round-1 student-error mutant. The Student-t scale uses the reciprocal of the matched factor, nu / (nu - 2), instead of (nu - 2) / nu.",
        "            scale = math.sqrt(matched * nu / chi_square)",
        "            scale = math.sqrt(nu / (matched * chi_square))",
    ),
]


def main() -> int:
    reference = REFERENCE.read_text(encoding="utf-8")
    for stem, description, old, new in SUBSTITUTIONS:
        count = reference.count(old)
        if count != 1:
            raise SystemExit(f"{stem}: the substitution matches {count} times in the reference (must be exactly 1)")
        body = reference.replace(old, new)
        head, sep, rest = body.partition('"""')
        if not sep:
            raise SystemExit(f"{stem}: no module docstring found")
        docstring_body, close, tail = rest.partition('"""')
        # Replace the module docstring's first line with the description so mutate_graders.py reads it.
        first_line, _, remainder = docstring_body.partition("\n")
        new_docstring = f"{description}\n{remainder}" if remainder else f"{description}\n"
        mutant = f"{head}{sep}{new_docstring}{close}{tail}"
        (MUTANTS / f"{stem}.py").write_text(mutant, encoding="utf-8")
        print(f"wrote {stem}.py ({first_line[:40]!r} replaced)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
