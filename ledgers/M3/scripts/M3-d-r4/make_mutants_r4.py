"""Round-4 verifier: write four new student-error mutants of the M3 reference under ledgers/M3/mutants/.

Each mutant is the reference with one exact replacement (asserted to match exactly once) and a new first docstring
line naming the student error. Usage (from the checkout root): .venv/bin/python -I ledgers/M3/scripts/M3-d-r4/make_mutants_r4.py
"""

from pathlib import Path

ROOT = Path.cwd()
REF = ROOT / "course/modules/M/M3/grader/reference.py"
OUT = ROOT / "ledgers/M3/mutants"
HEADER_OLD = '"""Reference solution for the M3 project, covariance_doctor.py. Not shipped to learners.\n'

MUTANTS = {
    "v4d_01_clip_repair_skips_rescale_when_nearly_unit_diagonal.py": (
        "clip_repair skips the rescaling when the clipped diagonal is within 1e-3 of 1, so the diagonal is not forced to 1.",
        "    return _rescale(x)\n",
        "    if all(abs(x[i][i] - 1.0) <= 1e-3 for i in range(len(x))):\n        return x\n    return _rescale(x)\n",
    ),
    "v4d_02_is_psd_tests_the_clipped_matrix.py": (
        "is_psd tests the eigenvalues of clip_repair(matrix) instead of those of the matrix it is given.",
        "    return min_eigenvalue(matrix) >= -tol\n",
        "    return min_eigenvalue(clip_repair(matrix)) >= -tol\n",
    ),
    "v4d_03_comparison_weights_divides_by_asset_count.py": (
        "comparison_weights normalises by the number of assets instead of by the sum of the solution.",
        "    total = sum(solution)\n    return [x / total for x in solution]\n",
        "    total = float(n)\n    return [x / total for x in solution]\n",
    ),
    "v4d_04_comparison_weights_ignores_volatilities.py": (
        "comparison_weights ignores the volatilities and solves with the correlation matrix C instead of S C S.",
        "    sigma = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]\n",
        "    sigma = [[c[i][j] for j in range(n)] for i in range(n)]\n",
    ),
}

for name, (description, old, new) in MUTANTS.items():
    text = REF.read_text(encoding="utf-8")
    assert text.count(HEADER_OLD) == 1, name
    assert text.count(old) == 1, f"{name}: replacement target matches {text.count(old)} times"
    body = text.replace(HEADER_OLD, f'"""{description}\n\nMutant of the reference. Not shipped to learners.\n', 1)
    body = body.replace(old, new, 1)
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
