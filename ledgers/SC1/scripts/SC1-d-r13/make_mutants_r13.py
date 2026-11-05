"""Writes the round-13 grader mutants (ledgers/SC1/mutants/r13_*.py) from the reference solution, one edit each.

Each edit is asserted to apply exactly once, so a changed reference fails loudly here rather than writing a mutant
that no longer differs from the reference in the intended way.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/SC/SC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/SC1/mutants"


def edit(old: str, new: str) -> str:
    assert REF.count(old) == 1, f"edit anchor must occur exactly once: {old[:60]!r}"
    return REF.replace(old, new)


MUTANTS: dict[str, str] = {
    "r13_01_erfc_three_digit_approximation.py": edit(
        '"""Reference solution',
        '"""Reflection tail from the Abramowitz and Stegun 7.1.26 erfc approximation, error up to 1.5e-7, not erfc.\n\n'
        'Reference solution',
    ).replace(
        "    return math.erfc(a / math.sqrt(2.0 * t))\n",
        "    x = a / math.sqrt(2.0 * t)\n"
        "    z = abs(x)\n"
        "    u = 1.0 / (1.0 + 0.3275911 * z)\n"
        "    poly = u * (0.254829592 + u * (-0.284496736 + u * (1.421413741 + u * (-1.453152027 + u * 1.061405429))))\n"
        "    y = poly * math.exp(-z * z)\n"
        "    return y if x >= 0 else 2.0 - y\n",
    ),
    "r13_02_generator_cached_per_seed.py": edit(
        '"""Reference solution',
        '"""Keeps one generator per seed across calls, so a repeated call on the same instance continues the draws.\n\n'
        'Reference solution',
    ).replace(
        "    rng = random.Random(int(instance[\"seed\"]))\n    sd = math.sqrt(float(instance[\"H\"]) / n_steps)\n",
        "    key = int(instance[\"seed\"])\n"
        "    rng = _GENERATORS.setdefault(key, random.Random(key))\n"
        "    sd = math.sqrt(float(instance[\"H\"]) / n_steps)\n",
    ).replace(
        "def _grid_paths(",
        "_GENERATORS: dict[int, random.Random] = {}\n\n\ndef _grid_paths(",
    ),
    "r13_03_two_paths_rejected.py": edit(
        '    if int(instance["n_paths"]) < 2:\n        raise ValueError("the estimate needs at least two paths for a standard error")\n',
        '    if int(instance["n_paths"]) < 3:\n        raise ValueError("the estimate needs at least three paths for a standard error")\n',
    ).replace(
        '"""Reference solution',
        '"""Rejects two paths, which the page allows, by demanding three paths before a standard error is computed.\n\n'
        'Reference solution',
    ),
    "r13_04_increment_variance_ignores_grid_size.py": edit(
        '    sd = math.sqrt(float(instance["H"]) / n_steps)\n',
        '    sd = math.sqrt(float(instance["H"]))\n',
    ).replace(
        '"""Reference solution',
        '"""Draws every increment with variance H, not H / n_steps, so each grid is coarser than its step count says.\n\n'
        'Reference solution',
    ),
    "r13_05_srw_terminal_count_returns_float.py": edit(
        '    return sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a)\n',
        '    return float(sum(math.comb(n, j) for j in range(n + 1) if 2 * j - n >= a))\n',
    ).replace(
        '"""Reference solution',
        '"""Returns the endpoint count as a float, so the count is not an exact integer as the page requires.\n\n'
        'Reference solution',
    ),
}

if __name__ == "__main__":
    for name, text in MUTANTS.items():
        (OUT / name).write_text(text, encoding="utf-8")
        print("wrote", name)
