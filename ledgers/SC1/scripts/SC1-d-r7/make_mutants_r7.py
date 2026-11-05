"""Round 7 (SC1-d): write four new student-error mutants of reference.py into ledgers/SC1/mutants/.

Each mutant is reference.py with exactly one textual change; the script asserts that the target text occurs once.
Run from the checkout root: .venv/bin/python -I ledgers/SC1/scripts/SC1-d-r7/make_mutants_r7.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REF = (ROOT / "course/modules/SC/SC1/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/SC1/mutants"

MUTANTS = {
    "m38_reflection_tail_accepts_zero_level": (
        "Boundary slip: reflection_tail accepts a = 0 (guard a < 0 instead of a <= 0) and returns erfc(0) = 1.",
        "    if a <= 0:\n        raise ValueError(\"the level a must be positive for the reflection tail\")",
        "    if a < 0:\n        raise ValueError(\"the level a must be positive for the reflection tail\")",
    ),
    "m39_standard_error_divided_by_sqrt_n_minus_one": (
        "Denominator slip: discrete_max_exceedance divides the sample standard deviation by sqrt(N - 1) instead of sqrt(N).",
        "    return mean, math.sqrt(variance) / math.sqrt(count)",
        "    return mean, math.sqrt(variance) / math.sqrt(count - 1)",
    ),
    "m40_box_muller_instead_of_gauss": (
        "Generator slip: the grid increments come from a hand-written Box-Muller transform of rng.random(), not from "
        "rng.gauss as the page states.",
        "            position += rng.gauss(0.0, sd)",
        "            u1 = 1.0 - rng.random()\n"
        "            u2 = rng.random()\n"
        "            position += sd * math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)",
    ),
    "m41_tail_uses_phi_at_a_over_root_2t": (
        "Function confusion: reflection_tail returns 2 (1 - Phi(a / sqrt(2 t))) with the normal cdf, not erfc(a / sqrt(2 t)).",
        "    return math.erfc(a / math.sqrt(2.0 * t))",
        "    z = a / math.sqrt(2.0 * t)\n    return 2.0 * (1.0 - 0.5 * (1.0 + math.erf(z / math.sqrt(2.0))))",
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    assert REF.count(old) == 1, (name, REF.count(old))
    body = REF.replace(old, new, 1)
    first, rest = body.split('"""', 1)[0], body.split('"""', 2)
    # Replace the module docstring (the first triple-quoted block) with the error description.
    end = body.index('"""', body.index('"""') + 3) + 3
    module = f'"""{doc}\n\nMutant of reference.py: exactly one change, as described above.\n"""' + body[end:]
    (OUT / f"{name}.py").write_text(module, encoding="utf-8")
    print("wrote", name)
