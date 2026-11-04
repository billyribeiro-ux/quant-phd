"""Write round-3 student-error mutants of the SC1 reference into ledgers/SC1/mutants/.

Each mutant is reference.py with one edit; the docstring's first line names the error. Run from the repo root:
    .venv/bin/python ledgers/SC1/scripts/SC1-d-r3/make_mutants_r3.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/SC/SC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/SC1/mutants"

HEADER_OLD = REF.split('"""', 2)[1]  # the module docstring body (first triple-quoted block)

MUTANTS = {
    "m22_seed_offset_by_one": (
        "Seed offset: _grid_paths draws from random.Random(seed + 1), a different sample from the instance's seed.",
        ('rng = random.Random(int(instance["seed"]))', 'rng = random.Random(int(instance["seed"]) + 1)'),
    ),
    "m23_srw_terminal_odd_shortcut": (
        "Odd-length shortcut: srw_terminal_count returns 2**(n - 1) for every level a whenever n is odd.",
        (
            '    if a < 1:\n        raise ValueError("the level a must be at least 1")\n    return sum(',
            '    if a < 1:\n        raise ValueError("the level a must be at least 1")\n'
            "    if n % 2:\n        return 2 ** (n - 1)\n    return sum(",
        ),
    ),
    "m24_standard_error_divided_by_n": (
        "Standard error divided by N instead of sqrt(N): the error bar is too narrow by a factor of sqrt(N).",
        ("return mean, math.sqrt(variance) / math.sqrt(count)", "return mean, math.sqrt(variance) / count"),
    ),
    "m25_increment_scale_sqrt_h_over_n_misplaced": (
        "Increment scale: the standard deviation is sqrt(H) / n_steps instead of sqrt(H / n_steps).",
        ("sd = math.sqrt(float(instance[\"H\"]) / n_steps)", 'sd = math.sqrt(float(instance["H"])) / n_steps'),
    ),
    "m26_srw_max_reflection_uses_endpoint_at_a": (
        "Reflection term misplaced: srw_max_count adds the endpoint count at a twice instead of at a + 1.",
        (
            "return srw_terminal_count(n, a) + srw_terminal_count(n, a + 1)",
            "return srw_terminal_count(n, a) + srw_terminal_count(n, a)",
        ),
    ),
}

for name, (description, (old, new)) in MUTANTS.items():
    if REF.count(old) != 1:
        raise SystemExit(f"{name}: pattern found {REF.count(old)} times, expected 1")
    text = REF.replace(old, new, 1)
    head_old = '"""' + HEADER_OLD + '"""'
    text = text.replace(head_old, f'"""{description}"""', 1)
    (OUT / f"{name}.py").write_text(text, encoding="utf-8")
    print("wrote", name)
