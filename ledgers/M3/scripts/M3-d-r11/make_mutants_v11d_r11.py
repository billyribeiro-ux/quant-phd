"""Round-11 verifier (M3 slice d): write three new student-error mutants of the M3 reference into ledgers/M3/mutants/.

Each mutant is reference.py with one plausible student error; each replacement must match exactly once (asserted).
Run from the checkout root: .venv/bin/python ledgers/M3/scripts/M3-d-r11/make_mutants_v11d_r11.py
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path.cwd()
REF = (ROOT / "course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
OUT = ROOT / "ledgers/M3/mutants"
DOC_OLD = '"""Reference solution for the M3 project, covariance_doctor.py. Not shipped to learners.'

MUTANTS: dict[str, list[tuple[str, str]]] = {
    "v11d_01_projection_pins_psd_iterate_diagonal_before_correction.py": [
        (
            DOC_OLD,
            '"""projection_repair pins the diagonal of the PSD step to one before the correction term is formed.',
        ),
        (
            "        corr_s = [[x[i][j] + corr_s[i][j] - y[i][j] for j in range(n)] for i in range(n)]",
            "        for i in range(n):\n"
            "            y[i][i] = 1.0\n"
            "        corr_s = [[x[i][j] + corr_s[i][j] - y[i][j] for j in range(n)] for i in range(n)]",
        ),
    ],
    "v11d_02_symmetry_tolerance_scaled_by_dimension.py": [
        (
            DOC_OLD,
            '"""_as_matrix scales the symmetry tolerance by the dimension, so a 2e-9 asymmetry passes in a 3 by 3 matrix.',
        ),
        (
            "            if abs(out[i][j] - out[j][i]) > SYMMETRY_TOL:",
            "            if abs(out[i][j] - out[j][i]) > SYMMETRY_TOL * n:",
        ),
    ],
    "v11d_03_rescale_uses_first_diagonal_entry.py": [
        (
            DOC_OLD,
            '"""_rescale divides entry (i, j) by sqrt(d_0 d_j), so the first diagonal entry replaces d_i in every row.',
        ),
        (
            "    return [[x[i][j] / math.sqrt(d[i] * d[j]) for j in range(len(x))] for i in range(len(x))]",
            "    return [[x[i][j] / math.sqrt(d[0] * d[j]) for j in range(len(x))] for i in range(len(x))]",
        ),
    ],
}

for name, replacements in MUTANTS.items():
    text = REF
    for old, new in replacements:
        assert text.count(old) == 1, (name, old[:60], text.count(old))
        text = text.replace(old, new)
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)
