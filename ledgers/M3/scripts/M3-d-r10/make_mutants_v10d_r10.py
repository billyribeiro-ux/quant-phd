"""Round-10 verifier (M3 slice d): write four new student-error mutants of the M3 reference into ledgers/M3/mutants/.

Each mutant is reference.py with one plausible student error, and each replacement must match exactly once (asserted),
so the mutation is real. Run from the checkout root: .venv/bin/python ledgers/M3/scripts/M3-d-r10/make_mutants_v10d_r10.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path.cwd()
REF = (ROOT / "course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M3/mutants"

MUTANTS: dict[str, list[tuple[str, str, str]]] = {
    # name -> list of (old, new, docstring-line) ; the first replacement rewrites the module docstring's first line
    "v10d_01_projection_psd_step_uses_clipping_with_rescaling.py": [
        (
            '"""Reference solution for the M3 project, covariance_doctor.py. Not shipped to learners.',
            '"""projection_repair uses clipping with rescaling as its PSD step, so each step returns a unit-diagonal matrix.',
            "docstring",
        ),
        (
            "        y = _psd_projection([[x[i][j] + corr_s[i][j] for j in range(n)] for i in range(n)])",
            "        y = _rescale(_rebuild(*_eigh_clip([[x[i][j] + corr_s[i][j] for j in range(n)] for i in range(n)])))",
            "code",
        ),
        (
            "def _rescale(x: Matrix) -> Matrix:",
            "def _eigh_clip(a: Matrix) -> tuple[list[float], Matrix]:\n"
            "    values, vectors = _eigh(a)\n"
            "    return [max(value, 0.0) for value in values], vectors\n\n\n"
            "def _rescale(x: Matrix) -> Matrix:",
            "code",
        ),
    ],
    "v10d_02_min_eigenvalue_reads_lower_triangle_without_symmetry_check.py": [
        (
            '"""Reference solution for the M3 project, covariance_doctor.py. Not shipped to learners.',
            '"""min_eigenvalue skips the symmetry test and reads only the lower triangle, so an asymmetry beyond 1e-9 is accepted.',
            "docstring",
        ),
        (
            "    values, _ = _eigh(_as_matrix(matrix))\n    return min(values)",
            "    rows = [list(row) for row in matrix]\n"
            "    n = len(rows)\n"
            "    full = [[rows[i][j] if j <= i else rows[j][i] for j in range(n)] for i in range(n)]\n"
            "    values, _ = _eigh(full)\n"
            "    return min(values)",
            "code",
        ),
    ],
    "v10d_03_projection_returns_the_iterate_before_the_last_step.py": [
        (
            '"""Reference solution for the M3 project, covariance_doctor.py. Not shipped to learners.',
            '"""projection_repair returns the iterate before the last step (one step short of max_iter), an off-by-one in the return.',
            "docstring",
        ),
        (
            "    for _ in range(max_iter):\n        y = _psd_projection(",
            "    previous = x\n    for _ in range(max_iter):\n        previous = x\n        y = _psd_projection(",
            "code",
        ),
        (
            "        if gap <= tol and step <= tol:\n            break\n    return x",
            "        if gap <= tol and step <= tol:\n            break\n    return previous",
            "code",
        ),
    ],
    "v10d_04_comparison_sigma_scales_only_the_column_volatility.py": [
        (
            '"""Reference solution for the M3 project, covariance_doctor.py. Not shipped to learners.',
            '"""comparison_weights uses Sigma_ij = C_ij v_j^2 (column volatility only), so Sigma is not S C S.',
            "docstring",
        ),
        (
            "    sigma = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]",
            "    sigma = [[c[i][j] * float(vols[j]) ** 2 for j in range(n)] for i in range(n)]",
            "code",
        ),
    ],
}

for name, edits in MUTANTS.items():
    text = REF
    for old, new, _kind in edits:
        count = text.count(old)
        assert count == 1, f"{name}: expected one match for {old[:60]!r}, found {count}"
        text = text.replace(old, new)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
