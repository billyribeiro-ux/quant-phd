"""Round-6 verifier (the unit-diagonal correction variants were dropped: they are equivalent to v5d_01, see notes): new student-error mutants of the M3 reference, written to ledgers/M3/mutants/.

Each mutant is the reference with one edit; every edit is asserted to match exactly once.
Usage (from the checkout root): .venv/bin/python -I ledgers/M3/scripts/M3-d-r6/make_mutants_r6.py
"""

from pathlib import Path

ROOT = Path.cwd()
REF = ROOT / "course/modules/M/M3/grader/reference.py"
OUT = ROOT / "ledgers/M3/mutants"
src = REF.read_text(encoding="utf-8")

MUTANTS = {
    "r6d_m02_projection_starts_from_clipped_input.py": (
        "projection_repair starts the alternating steps from the PSD projection of the input instead of the input.",
        "    a = _as_matrix(matrix)\n    n = len(a)\n    x = a\n",
        "    a = _as_matrix(matrix)\n    n = len(a)\n    x = _psd_projection(a)\n",
    ),
    "r6d_m03_comparison_weights_unit_euclidean_norm.py": (
        "comparison_weights scales the solution to unit Euclidean length instead of to sum one.",
        "    total = sum(solution)\n    return [x / total for x in solution]\n",
        "    total = sum(x * x for x in solution) ** 0.5\n    return [x / total for x in solution]\n",
    ),
    "r6d_m04_symmetrise_by_sum_not_average.py": (
        "_as_matrix symmetrises by summing the two entries m[i][j] and m[j][i] instead of averaging them.",
        "    return [[(out[i][j] + out[j][i]) / 2.0 for j in range(n)] for i in range(n)]\n",
        "    return [[(out[i][j] + out[j][i]) for j in range(n)] for i in range(n)]\n",
    ),
}

for name, (description, old, new) in MUTANTS.items():
    assert src.count(old) == 1, f"edit for {name} matches {src.count(old)} times"
    text = src.replace(old, new, 1)
    body = f'"""{description}"""\n' + text.split('"""', 2)[2]
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
