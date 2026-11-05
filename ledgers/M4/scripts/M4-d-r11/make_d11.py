"""Write the round-11 verifier mutants (ledgers/M4/mutants/d11_*.py) and alternatives (scripts/M4-d-r11/alts/).

Each mutant is the reference solution with one targeted edit; every edit must match exactly once, or the script fails.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/M/M4/grader/reference.py").read_text(encoding="utf-8")
MUT = ROOT / "ledgers/M4/mutants"
ALT = ROOT / "ledgers/M4/scripts/M4-d-r11/alts"


def edit(src: str, old: str, new: str) -> str:
    n = src.count(old)
    if n != 1:
        raise SystemExit(f"edit target found {n} times: {old[:60]!r}")
    return src.replace(old, new)


MUTANTS = {
    "d11_01_short_positions_rejected_as_invalid.py": (
        '"""Round-11 verifier student-error mutant: simulate_losses rejects a negative position, so a short position raises\n'
        'ValueError although the page says a short position is valid input."""\n',
        [
            (
                '    n = len(position_cents)\n    factor = _cholesky(cov, n)\n',
                '    if any(w < 0 for w in position_cents):\n'
                '        raise ValueError("position_cents must be non-negative: a short position is not allowed")\n'
                '    n = len(position_cents)\n    factor = _cholesky(cov, n)\n',
            ),
        ],
    ),
    "d11_02_gaussian_normals_drawn_position_major.py": (
        '"""Round-11 verifier student-error mutant: the Gaussian normals are drawn position-major (all draws of asset 1,\n'
        'then all draws of asset 2), so each draw takes its z from the wrong place in the stream."""\n',
        [
            (
                '    for _ in range(n_draws):\n        z = [rng.gauss(0.0, 1.0) for _ in range(n)]\n',
                '    flat = [rng.gauss(0.0, 1.0) for _ in range(n * n_draws)] if family == "gaussian" else []\n'
                '    for d in range(n_draws):\n'
                '        z = [flat[i * n_draws + d] for i in range(n)] if family == "gaussian" else [\n'
                '            rng.gauss(0.0, 1.0) for _ in range(n)\n'
                '        ]\n',
            ),
        ],
    ),
    "d11_03_gaussian_normals_from_inverse_cdf_of_random.py": (
        '"""Round-11 verifier student-error mutant: the Gaussian normals are the inverse CDF of rng.random(), a standard\n'
        'normal but not the frozen random.Random(seed).gauss stream the page specifies."""\n',
        [
            (
                '    for _ in range(n_draws):\n        z = [rng.gauss(0.0, 1.0) for _ in range(n)]\n',
                '    import statistics\n\n    std = statistics.NormalDist()\n'
                '    for _ in range(n_draws):\n'
                '        z = [std.inv_cdf(rng.random()) if family == "gaussian" else rng.gauss(0.0, 1.0)\n'
                '             for _ in range(n)]\n',
            ),
        ],
    ),
    "d11_04_quantile_index_from_n_minus_one.py": (
        '"""Round-11 verifier student-error mutant: quantile_99 takes the ceiling index of 0.99 times (n - 1), one\n'
        'order statistic low once n is at least 101 (for example at n = 101 it returns the 99th loss, not the 100th)."""\n',
        [
            (
                '    index = (99 * len(losses_cents) + 99) // 100\n',
                '    index = (99 * (len(losses_cents) - 1) + 99) // 100\n',
            ),
        ],
    ),
}

ALTERNATIVES = {
    # Student-t chi-square drawn before the normals of each draw; the Gaussian stream is untouched. Order open (item 5).
    "alt_d11_1_student_t_chi_square_before_normals.py": (REF, [
        (
            '        z = [rng.gauss(0.0, 1.0) for _ in range(n)]\n        scale = 1.0\n        if student and nu is not None:\n'
            '            chi_square = rng.gammavariate(nu / 2, 2.0)\n            scale = math.sqrt(matched * nu / chi_square)\n',
            '        scale = 1.0\n        if student and nu is not None:\n'
            '            chi_square = rng.gammavariate(nu / 2, 2.0)\n            scale = math.sqrt(matched * nu / chi_square)\n'
            '        z = [rng.gauss(0.0, 1.0) for _ in range(n)]\n',
        ),
    ]),
    # Student-t chi-square variables come from a second generator seeded seed + 1; still one independent W per draw.
    "alt_d11_2_student_t_chi_square_from_second_generator.py": (REF, [
        (
            '    rng = random.Random(seed)\n',
            '    rng = random.Random(seed)\n    chi_rng = random.Random(seed + 1)\n',
        ),
        (
            '            chi_square = rng.gammavariate(nu / 2, 2.0)\n',
            '            chi_square = chi_rng.gammavariate(nu / 2, 2.0)\n',
        ),
    ]),
    # Different algorithms and cutoffs: heapq selection, exact Fraction index, matched scale as 1 - 2 / nu,
    # pivot test with math.isfinite and an explicit strict comparison, symmetry by exact equality of floats.
    "alt_d11_3_heapq_fraction_index_and_selection_factor.py": (REF, [
        (
            '    index = (99 * len(losses_cents) + 99) // 100\n    return sorted(losses_cents)[index - 1]\n',
            '    import heapq\n    from fractions import Fraction\n\n'
            '    index = math.ceil(Fraction(99, 100) * len(losses_cents))\n'
            '    return heapq.nsmallest(index, losses_cents)[-1]\n',
        ),
        (
            '    return (nu - 2) / nu\n',
            '    return 1.0 - 2.0 / nu\n',
        ),
        (
            '                if not pivot > 0.0:\n',
            '                if not (math.isfinite(pivot) and pivot > 0.0):\n',
        ),
    ]),
}


def write(folder: Path, name: str, text: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / name).write_text(text, encoding="utf-8")


def main() -> None:
    # The reference is a module docstring followed by the code; a mutant replaces the docstring and edits the code.
    body_of_reference = REF.split('"""', 2)[2]
    for name, (doc, edits) in MUTANTS.items():
        body = body_of_reference
        for old, new in edits:
            body = edit(body, old, new)
        write(MUT, name, doc + body)
    for name, (base, edits) in ALTERNATIVES.items():
        text = base
        for old, new in edits:
            text = edit(text, old, new)
        write(ALT, name, text)
    print("written", len(MUTANTS), "mutants and", len(ALTERNATIVES), "alternatives")


if __name__ == "__main__":
    main()
