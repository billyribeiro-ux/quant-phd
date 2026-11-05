"""Round-9 verifier (M3 slice d): writes four new student-error mutants of the reference into ledgers/M3/mutants/ as
v9d_01..v9d_04. Each mutant is grader/reference.py with the listed edits only; every edit target must occur exactly once.
Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-d-r9/make_mutants_v9d_r9.py
"""

from pathlib import Path

ROOT = Path.cwd()
REF = (ROOT / "course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M3/mutants"

HEADER_OLD = '''"""Reference solution for the M3 project, covariance_doctor.py. Not shipped to learners.

Pure Python, standard library only. Eigenvalues come from cyclic Jacobi rotations; the projection repair is computed by
alternating projections, with correction terms, between the positive semidefinite and the unit-diagonal matrices.
"""'''


def build(description, edits):
    assert REF.count(HEADER_OLD) == 1, "reference header changed"
    text = REF.replace(
        HEADER_OLD,
        f'"""{description}\n\nA student-error mutant of grader/reference.py: the listed edits only, nothing else changed.\n"""',
    )
    for old, new in edits:
        assert text.count(old) == 1, f"edit target not unique: {old[:70]!r}"
        text = text.replace(old, new)
    return text


IS_PSD_OLD = '''def is_psd(matrix: list[list[float]], tol: float = 1e-10) -> bool:
    """True when every eigenvalue of the symmetric matrix is at least -tol."""
    return min_eigenvalue(matrix) >= -tol'''
IS_PSD_NEW = '''def _pivots_positive(m: Matrix) -> bool:
    n = len(m)
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            total = sum(low[i][k] * low[j][k] for k in range(j))
            if i == j:
                pivot = m[i][i] - total
                if not pivot > 0.0:
                    return False
                low[i][i] = math.sqrt(pivot)
            else:
                low[i][j] = (m[i][j] - total) / low[j][j]
    return True


def is_psd(matrix: list[list[float]], tol: float = 1e-10) -> bool:
    """True when every eigenvalue of the symmetric matrix is at least -tol."""
    a = _as_matrix(matrix)
    n = len(a)
    return _pivots_positive([[a[i][j] + (tol if i == j else 0.0) for j in range(n)] for i in range(n)])'''

MUTANTS = {
    "v9d_01_is_psd_is_pd_of_shifted_matrix_refuses_boundary.py": (
        "is_psd tests whether matrix plus tol times the identity is positive definite by strictly positive pivots, "
        "so an eigenvalue exactly at -tol and a planted zero eigenvalue are refused.",
        [(IS_PSD_OLD, IS_PSD_NEW)],
    ),
    "v9d_02_min_eigenvalue_is_smallest_in_absolute_value.py": (
        "min_eigenvalue returns the eigenvalue of smallest absolute value, not the smallest eigenvalue.",
        [("    values, _ = _eigh(_as_matrix(matrix))\n    return min(values)", "    values, _ = _eigh(_as_matrix(matrix))\n    return min(values, key=abs)")],
    ),
    "v9d_03_weights_normalised_by_absolute_sum.py": (
        "comparison_weights divides by the sum of the absolute values of the solution, so the weights need not sum to 1.",
        [("    total = sum(solution)\n    return [x / total for x in solution]", "    total = sum(abs(x) for x in solution)\n    return [x / total for x in solution]")],
    ),
    "v9d_04_clip_rescales_by_input_diagonal.py": (
        "clip_repair rescales by the diagonal of the input rather than the diagonal of the clipped matrix.",
        [(
            "    x = _rebuild([max(value, floor) for value in values], vectors)\n    return _rescale(x)",
            "    x = _rebuild([max(value, floor) for value in values], vectors)\n    d = [a[i][i] for i in range(len(a))]\n    return [[x[i][j] / math.sqrt(d[i] * d[j]) for j in range(len(x))] for i in range(len(x))]",
        )],
    ),
}

if __name__ == "__main__":
    for name, (description, edits) in MUTANTS.items():
        text = build(description, edits)
        target = OUT / name
        if target.exists() and target.read_text(encoding="utf-8") == text:
            print("identical", name)
        else:
            target.write_text(text, encoding="utf-8")
            print("wrote", name)
