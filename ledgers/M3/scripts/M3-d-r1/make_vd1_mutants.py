"""Write the verifier's round-1 student-error mutants (vd1_01..vd1_04) from the M3 reference, one edit each."""

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD1-M3-d")
SRC = (ROOT / "course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M3/mutants"

MUTANTS = {
    "vd1_01_comparison_weights_refuses_non_psd_correlation.py": (
        "comparison_weights refuses a correlation matrix that is not positive semidefinite, which the formula does not need.",
        '    c = _as_matrix(corr)\n    n = len(c)\n',
        '    c = _as_matrix(corr)\n    n = len(c)\n    if not is_psd(c):\n        raise ValueError("the correlation matrix is not positive semidefinite")\n',
    ),
    "vd1_02_clip_repair_refuses_negative_floor.py": (
        "clip_repair refuses a negative floor with ValueError, although the signature allows any floor.",
        '    a = _as_matrix(matrix)\n    values, vectors = _eigh(a)\n    x = _rebuild([max(value, floor)',
        '    if floor < 0.0:\n        raise ValueError("the floor must not be negative")\n    a = _as_matrix(matrix)\n    values, vectors = _eigh(a)\n    x = _rebuild([max(value, floor)',
    ),
    "vd1_03_is_psd_refuses_zero_diagonal_entry.py": (
        "is_psd returns False whenever a diagonal entry is exactly zero, although diag(0, 1, 1) is positive semidefinite.",
        '    return min_eigenvalue(matrix) >= -tol\n',
        '    if any(float(matrix[i][i]) == 0.0 for i in range(len(matrix))):\n        return False\n    return min_eigenvalue(matrix) >= -tol\n',
    ),
    "vd1_04_min_eigenvalue_uses_only_upper_triangle_for_symmetry.py": (
        "_as_matrix checks symmetry only for pairs with i below j in the first row, so asymmetry in later rows passes.",
        '    for i in range(n):\n        for j in range(i + 1, n):\n            if abs(out[i][j] - out[j][i]) > SYMMETRY_TOL:',
        '    for i in range(min(n, 1)):\n        for j in range(i + 1, n):\n            if abs(out[i][j] - out[j][i]) > SYMMETRY_TOL:',
    ),
}

for name, (doc, old, new) in MUTANTS.items():
    assert SRC.count(old) == 1, (name, SRC.count(old))
    body = SRC.replace(old, new, 1)
    start = body.index('"""')
    end = body.index('"""', start + 3) + 3
    body = f'"""{doc}"""\n' + body[end:]
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
