"""Write this round's new student-error mutants (verifier scratch) from the reference, one exact replacement each.

The in-place writes come AFTER the validation call, so an asymmetric-within-tolerance argument reaches the write
and the only observable difference is the mutation of the caller's argument.
"""

from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyD3-M3-d")
REF = (ROOT / "course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M3/mutants"
OPEN = '"""Reference solution for the M3 project, covariance_doctor.py. Not shipped to learners.'


def swap(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f"anchor not unique: {old[:60]!r}"
    return text.replace(old, new)


def symm_in_place(name: str) -> str:
    return (
        f"    if all(len({name}[r]) == len({name}) for r in range(len({name}))):\n"
        f"        for i in range(len({name})):\n"
        f"            for j in range(i + 1, len({name})):\n"
        f"                {name}[i][j] = {name}[j][i] = ({name}[i][j] + {name}[j][i]) / 2.0\n"
    )


MUTANTS = {
    # 1. comparison_weights symmetrises the caller's correlation matrix in place, after validating it.
    "vd3_01_comparison_weights_symmetrises_caller_corr_in_place.py": (
        "comparison_weights writes the symmetrised average back into the caller's correlation matrix, "
        "which the page forbids.",
        swap(
            REF,
            "    c = _as_matrix(corr)\n    n = len(c)\n    if len(vols) != n:",
            "    c = _as_matrix(corr)\n    n = len(c)\n" + symm_in_place("corr") + "    if len(vols) != n:",
        ),
    ),
    # 2. min_eigenvalue symmetrises the caller's matrix in place, after validating it.
    "vd3_02_min_eigenvalue_symmetrises_caller_matrix_in_place.py": (
        "min_eigenvalue writes the symmetrised average back into the caller's matrix, which the page forbids.",
        swap(
            REF,
            "    values, _ = _eigh(_as_matrix(matrix))\n    return min(values)",
            "    _as_matrix(matrix)\n" + symm_in_place("matrix") + "    values, _ = _eigh(_as_matrix(matrix))\n    return min(values)",
        ),
    ),
    # 3. is_psd symmetrises the caller's matrix in place, after validating it.
    "vd3_03_is_psd_symmetrises_caller_matrix_in_place.py": (
        "is_psd writes the symmetrised average back into the caller's matrix, which the page forbids.",
        swap(
            REF,
            "    return min_eigenvalue(matrix) >= -tol",
            "    _as_matrix(matrix)\n" + symm_in_place("matrix") + "    return min_eigenvalue(matrix) >= -tol",
        ),
    ),
    # 4. min_eigenvalue uses SciPy, which the page does not allow (standard library and NumPy only).
    "vd3_04_min_eigenvalue_uses_scipy_not_allowed_by_page.py": (
        "min_eigenvalue calls scipy.linalg.eigvalsh, but the page allows only the standard library and NumPy.",
        swap(
            REF,
            "    values, _ = _eigh(_as_matrix(matrix))\n    return min(values)",
            "    import scipy.linalg\n\n    values = [float(x) for x in scipy.linalg.eigvalsh(_as_matrix(matrix))]\n    return min(values)",
        ),
    ),
}

for name, (desc, text) in MUTANTS.items():
    assert text.count(OPEN) == 1, name
    text = text.replace(OPEN, '"""' + desc + "\n\nMutant of the reference. Not shipped to learners.", 1)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name, len(text))
