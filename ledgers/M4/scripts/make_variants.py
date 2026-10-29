#!/usr/bin/env python3
"""Generate the five alternative correct implementations and the student-error mutants of the M4 project.

Each variant is the reference (course/modules/M/M4/grader/reference.py) with one explicit substitution. A
substitution must match exactly once in the reference, or the generator stops, so no variant can silently be the
reference itself.

* alt_1 .. alt_5 (ledgers/M4/scripts/): correct implementations that differ in algorithm or random stream. They
  must pass the whole suite on seeds 0-49 (run_alternatives.py).
* ledgers/M4/mutants/*.py: single-change copies of the reference, each with a one-line description as its first
  docstring line (mutate_graders.py reads it).

Usage::

    python3 ledgers/M4/scripts/make_variants.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REFERENCE = ROOT / "course/modules/M/M4/grader/reference.py"
SCRIPTS = Path(__file__).resolve().parent
MUTANTS = ROOT / "ledgers/M4/mutants"

NORMALS_BOX_MULLER = '''def _normals(rng: random.Random, n: int) -> list[float]:
    """n standard normals by the Box-Muller transform of pairs of uniforms."""
    out: list[float] = []
    while len(out) < n:
        u1 = 1.0 - rng.random()
        u2 = rng.random()
        radius = math.sqrt(-2.0 * math.log(u1))
        out.append(radius * math.cos(2.0 * math.pi * u2))
        out.append(radius * math.sin(2.0 * math.pi * u2))
    return out[:n]


def simulate_losses('''

NORMALS_POLAR = '''def _normals(rng: random.Random, n: int) -> list[float]:
    """n standard normals by the Marsaglia polar method, rejecting points outside the unit disc."""
    out: list[float] = []
    while len(out) < n:
        x = 2.0 * rng.random() - 1.0
        y = 2.0 * rng.random() - 1.0
        s = x * x + y * y
        if 0.0 < s < 1.0:
            factor = math.sqrt(-2.0 * math.log(s) / s)
            out.append(x * factor)
            out.append(y * factor)
    return out[:n]


def simulate_losses('''

CHOLESKY_COLUMNS = """    factor = [[0.0] * n for _ in range(n)]
    for j in range(n):
        pivot = cov[j][j] - sum(factor[j][k] ** 2 for k in range(j))
        if not pivot > 0.0:
            raise ValueError("cov must be positive definite: every Cholesky pivot must be above zero")
        factor[j][j] = math.sqrt(pivot)
        for i in range(j + 1, n):
            factor[i][j] = (cov[i][j] - sum(factor[i][k] * factor[j][k] for k in range(j))) / factor[j][j]
    return factor
"""

# Each entry: (name, description, [(old, new), ...]). Alternatives are listed separately below.
ALTERNATIVES: list[tuple[str, list[tuple[str, str]]]] = [
    (
        "alt_1",
        [
            ("def simulate_losses(", NORMALS_BOX_MULLER),
            ("z = [rng.gauss(0.0, 1.0) for _ in range(n)]", "z = _normals(rng, n)"),
        ],
    ),
    (
        "alt_2",
        [
            ("def simulate_losses(", NORMALS_POLAR),
            ("z = [rng.gauss(0.0, 1.0) for _ in range(n)]", "z = _normals(rng, n)"),
        ],
    ),
    (
        "alt_3",
        [
            (
                '    factor = [[0.0] * n for _ in range(n)]\n    for i in range(n):\n        for j in range(i + 1):\n            inner = sum(factor[i][k] * factor[j][k] for k in range(j))\n            if i == j:\n                pivot = cov[i][i] - inner\n                if not pivot > 0.0:\n                    raise ValueError("cov must be positive definite: every Cholesky pivot must be above zero")\n                factor[i][i] = math.sqrt(pivot)\n            else:\n                factor[i][j] = (cov[i][j] - inner) / factor[j][j]\n    return factor\n',  # noqa: E501
                CHOLESKY_COLUMNS,
            )
        ],
    ),
    (
        "alt_4",
        [
            (
                "chi_square = rng.gammavariate(nu / 2, 2.0)",
                "chi_square = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu))",
            )
        ],
    ),
    (
        "alt_5",
        [
            (
                "    index = (99 * len(losses_cents) + 99) // 100\n    return sorted(losses_cents)[index - 1]",
                "    index = (99 * len(losses_cents) + 99) // 100\n    return heapq.nsmallest(index, losses_cents)[-1]",
            ),
            ("import math\n", "import heapq\nimport math\n"),
        ],
    ),
]

# Mutants: (file name, one-line description, [(old, new)]). Each is a student error, a single change.
MUTANT_LIST: list[tuple[str, str, list[tuple[str, str]]]] = [
    (
        "m01_student_t_not_rescaled",
        "Student-t draws are not rescaled by the matched factor, so the covariance is inflated by nu / (nu - 2).",
        [("scale = math.sqrt(matched * nu / chi_square)", "scale = math.sqrt(nu / chi_square)")],
    ),
    (
        "m02_matched_scale_accepts_nu_two",
        "matched_scale accepts nu = 2 (the guard is nu < 2), returning a zero scale instead of an error.",
        [("    if nu <= 2:", "    if nu < 2:")],
    ),
    (
        "m03_quantile_floor_index",
        "The quantile index is floor(0.99 n) instead of ceil(0.99 n), one order statistic too low.",
        [("    index = (99 * len(losses_cents) + 99) // 100", "    index = max(1, (99 * len(losses_cents)) // 100)")],
    ),
    (
        "m04_losses_as_floats",
        "Losses are returned as floats, not rounded to integer cents.",
        [("losses.append(round(-total))", "losses.append(-total)")],
    ),
    (
        "m05_quantile_read_from_top",
        "The 99% loss is read from the top of the ordering (the gain side is treated as the loss tail).",
        [("    return sorted(losses_cents)[index - 1]", "    return sorted(losses_cents, reverse=True)[index - 1]")],
    ),
    (
        "m06_seed_zero_hard_coded",
        "A hard-coded answer for seed 0: every loss is zero when the seed is 0.",
        [
            (
                "    rng = random.Random(seed)\n",
                "    if seed == 0:\n        return [0] * n_draws\n    rng = random.Random(seed)\n",
            )
        ],
    ),
    (
        "m07_singular_covariance_accepted",
        "The Cholesky check accepts a zero pivot, so a singular covariance is treated as valid.",
        [("                if not pivot > 0.0:", "                if pivot < 0.0:")],
    ),
    (
        "m08_one_draw_short",
        "The simulation makes one draw too few and returns n_draws - 1 losses.",
        [("    for _ in range(n_draws):\n        z =", "    for _ in range(n_draws - 1):\n        z =")],
    ),
    (
        "m09_quantile_interpolated",
        "The quantile is linear interpolation at 0.99 (n - 1), a float, not an order statistic.",
        [
            (
                "    index = (99 * len(losses_cents) + 99) // 100\n    return sorted(losses_cents)[index - 1]",
                "    ordered = sorted(losses_cents)\n    position = 0.99 * (len(ordered) - 1)\n    low = int(position)\n    high = min(low + 1, len(ordered) - 1)\n    return ordered[low] + (position - low) * (ordered[high] - ordered[low])",  # noqa: E501
            )
        ],
    ),
    (
        "m10_gaussian_accepts_degrees_of_freedom",
        "The gaussian family accepts a degrees-of-freedom argument and ignores it, instead of rejecting it.",
        [
            (
                '    if family == "gaussian" and nu is not None:\n        raise ValueError("nu must be None for the gaussian family")\n',  # noqa: E501
                "",
            )
        ],
    ),
    (
        "m11_loss_sign_flipped",
        "The loss sign is reversed: gains are reported as losses (returns enter with the wrong sign).",
        [("losses.append(round(-total))", "losses.append(round(total))")],
    ),
]


def substitute(name: str, source: str, pairs: list[tuple[str, str]]) -> str:
    """Apply each (old, new) pair to source; each old string must occur exactly once."""
    for old, new in pairs:
        count = source.count(old)
        if count != 1:
            raise SystemExit(f"{name}: expected exactly one match for a substitution, found {count}")
        source = source.replace(old, new)
    return source


def main() -> int:
    reference = REFERENCE.read_text(encoding="utf-8")
    header_end = reference.index('"""', 3) + 3
    body = reference[header_end:]
    for name, pairs in ALTERNATIVES:
        text = substitute(name, reference, pairs)
        (SCRIPTS / f"{name}.py").write_text(text, encoding="utf-8")
        print(f"wrote ledgers/M4/scripts/{name}.py")
    MUTANTS.mkdir(parents=True, exist_ok=True)
    for name, description, pairs in MUTANT_LIST:
        mutated_body = substitute(name, body, pairs)
        text = f'"""{description}"""{mutated_body}'
        (MUTANTS / f"{name}.py").write_text(text, encoding="utf-8")
        print(f"wrote ledgers/M4/mutants/{name}.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
