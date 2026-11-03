"""Write verifier D round-2 student-error mutants of the M4 reference into ledgers/M4/mutants/ (verifier D, round 2).

Each mutant is the reference with exactly one substitution. A substitution must match exactly once in the reference,
or the generator stops, so no mutant can silently equal the reference. The first docstring line describes the error.
Run from the checkout root: .venv/bin/python ledgers/M4/scripts/M4-d-r2/verifyD2_make_mutants.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REFERENCE = ROOT / "course/modules/M/M4/grader/reference.py"
MUTANTS = ROOT / "ledgers/M4/mutants"

# (file stem, first docstring line, old text, new text)
SUBSTITUTIONS: list[tuple[str, str, str, str]] = [
    (
        "v2_01_short_position_read_as_long",
        "Verifier round-2 student-error mutant. A short position is read as a long one: the loss uses the absolute value of each position.",
        "        total += position_cents[i] * ret",
        "        total += abs(position_cents[i]) * ret",
    ),
    (
        "v2_02_upper_factor_used_as_lower",
        "Verifier round-2 student-error mutant. The upper-triangular factor is used where the lower one belongs, so each return is L^T Z, not L Z.",
        "            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))",
        "            ret = scale * sum(factor[k][i] * z[k] for k in range(i, n))",
    ),
    (
        "v2_03_zero_pivot_accepted",
        "Verifier round-2 student-error mutant. The pivot test is written not-negative, so a zero variance is accepted as positive definite.",
        "                if not pivot > 0.0:",
        "                if not pivot >= 0.0:",
    ),
    (
        "v2_04_normals_drawn_in_reverse_position_order",
        "Verifier round-2 student-error mutant. The m standard normals of each draw are taken in reverse position order, not in position order.",
        "        z = [rng.gauss(0.0, 1.0) for _ in range(n)]",
        "        z = [rng.gauss(0.0, 1.0) for _ in range(n)][::-1]",
    ),
]


def main() -> None:
    reference = REFERENCE.read_text(encoding="utf-8")
    for stem, first_line, old, new in SUBSTITUTIONS:
        count = reference.count(old)
        if count != 1:
            raise SystemExit(f"{stem}: the substitution matches {count} times in the reference, expected exactly 1")
        body = reference.replace(old, new)
        body = body.replace(reference.splitlines()[0], '"""' + first_line, 1)
        path = MUTANTS / f"{stem}.py"
        path.write_text(body, encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
