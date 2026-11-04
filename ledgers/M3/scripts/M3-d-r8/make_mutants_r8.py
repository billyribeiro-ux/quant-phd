"""Round-8 verifier (M3 slice d): writes four student-error mutants of the reference into ledgers/M3/mutants/.

Each mutant is grader/reference.py with the listed edits, each asserted to match exactly once. The module docstring's
first line names the error. Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-d-r8/make_mutants_r8.py
"""

from pathlib import Path

ROOT = Path.cwd()
REF = (ROOT / "course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M3/mutants"

HEADER_OLD = '''"""Reference solution for the M3 project, covariance_doctor.py. Not shipped to learners.

Pure Python, standard library only. Eigenvalues come from cyclic Jacobi rotations; the projection repair is computed by
alternating projections, with correction terms, between the positive semidefinite and the unit-diagonal matrices.
"""'''


def build(description: str, edits: list[tuple[str, str]]) -> str:
    assert REF.count(HEADER_OLD) == 1, "reference header changed"
    text = REF.replace(
        HEADER_OLD,
        f'"""{description}\n\nA student-error mutant of grader/reference.py: the listed edits only, nothing else changed.\n"""',
    )
    for old, new in edits:
        assert text.count(old) == 1, f"edit target not unique: {old[:70]!r}"
        text = text.replace(old, new)
    return text


MUTANTS = {
    "v8d_01_is_psd_tolerance_scaled_by_largest_eigenvalue.py": build(
        "is_psd scales the tolerance by the largest eigenvalue magnitude, so a large diagonal loosens the PSD test.",
        [(
            "    return min_eigenvalue(matrix) >= -tol\n",
            "    values, _ = _eigh(_as_matrix(matrix))\n"
            "    return min(values) >= -tol * max(1.0, max(abs(v) for v in values))\n",
        )],
    ),
    "v8d_02_weights_ignore_the_correlation_entries.py": build(
        "comparison_weights treats the correlation matrix as the identity, so the weights ignore every correlation.",
        [(
            "    sigma = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]\n",
            "    sigma = [[float(vols[i]) * (1.0 if i == j else 0.0) * float(vols[j]) for j in range(n)] for i in range(n)]\n",
        )],
    ),
    "v8d_03_projection_refuses_one_by_one_matrix.py": build(
        "projection_repair refuses a one-by-one matrix with a ValueError that the page does not name.",
        [(
            "    n = len(a)\n    x = a\n",
            "    n = len(a)\n    if n == 1:\n        raise ValueError(\"projection_repair needs at least two rows\")\n    x = a\n",
        )],
    ),
    "v8d_04_projection_pins_unit_diagonal_only_after_last_step.py": build(
        "projection_repair pins the unit diagonal only once, after the last step, so each step projects without it.",
        [
            ("        for i in range(n):\n            new_x[i][i] = 1.0\n", ""),
            ("        if gap <= tol and step <= tol:\n            break\n    return x\n",
             "        if gap <= tol and step <= tol:\n            break\n"
             "    for i in range(n):\n        x[i][i] = 1.0\n    return x\n"),
        ],
    ),
}

for name, text in MUTANTS.items():
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
