"""Write the round-5 student-error mutants (d5_*) from the reference solution, one edit each."""

import pathlib

REF = pathlib.Path("/tmp/quant-b2/course/modules/M/M3/grader/reference.py")
OUT = pathlib.Path("/tmp/quant-b2/ledgers/M3/mutants")

MUTANTS = [
    ("d5_01_is_psd_default_tol_twelve.py",
     "is_psd with its default tolerance refuses a smallest eigenvalue of -1e-11 (default tol 1e-12, not 1e-10).",
     [("def is_psd(matrix: list[list[float]], tol: float = 1e-10)", "def is_psd(matrix: list[list[float]], tol: float = 1e-12)")]),
    ("d5_02_as_matrix_symmetrises_caller_in_place.py",
     "_as_matrix writes the symmetrised entries back into the caller's matrix, so an in-tolerance asymmetry is changed.",
     [("    return [[(out[i][j] + out[j][i]) / 2.0 for j in range(n)] for i in range(n)]",
       "    sym = [[(out[i][j] + out[j][i]) / 2.0 for j in range(n)] for i in range(n)]\n"
       "    for i in range(n):\n        for j in range(n):\n            matrix[i][j] = sym[i][j]\n    return sym")]),
    ("d5_03_clip_raises_only_negative_eigenvalues.py",
     "clip_repair sets only the negative eigenvalues to the floor, so a positive eigenvalue below a positive floor is kept.",
     [("x = _rebuild([max(value, floor) for value in values], vectors)",
       "x = _rebuild([floor if value < 0 else value for value in values], vectors)")]),
    ("d5_04_weights_take_absolute_volatility.py",
     "comparison_weights refuses only zero volatilities and uses |v| for a negative one, so a negative volatility is accepted.",
     [("if any(float(v) <= 0.0 for v in vols):", "if any(float(v) == 0.0 for v in vols):"),
      ("sigma = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]",
       "sigma = [[abs(float(vols[i])) * c[i][j] * abs(float(vols[j])) for j in range(n)] for i in range(n)]")]),
    ("d5_05_is_psd_rounds_the_eigenvalue.py",
     "is_psd compares the smallest eigenvalue rounded to six decimals, so -5e-9 rounds to zero and is accepted.",
     [("    return min_eigenvalue(matrix) >= -tol", "    return round(min_eigenvalue(matrix), 6) >= -tol")]),
    ("d5_06_min_eigenvalue_by_absolute_value.py",
     "min_eigenvalue returns the eigenvalue of smallest absolute value instead of the smallest eigenvalue.",
     [("    values, _ = _eigh(_as_matrix(matrix))\n    return min(values)",
       "    values, _ = _eigh(_as_matrix(matrix))\n    return min(values, key=abs)")]),
    ("d5_07_projection_skips_unit_diagonal_pin.py",
     "projection_repair does not pin the diagonal to one at each Dykstra step.",
     [("        for i in range(n):\n            new_x[i][i] = 1.0\n", "        pass\n")]),
    ("d5_08_non_square_checks_shorter_rows_only.py",
     "_as_matrix refuses a row shorter than the number of rows, but accepts a row that is longer.",
     [("    if any(len(row) != n for row in rows):", "    if any(len(row) < n for row in rows):")]),
    ("d5_09_weights_normalised_by_first_weight.py",
     "comparison_weights divides by the first unnormalised component, so the weights do not sum to one.",
     [("    total = sum(solution)", "    total = solution[0]")]),
    ("d5_10_weights_length_unchecked_when_empty.py",
     "comparison_weights skips the length check for an empty volatility list and fails with an IndexError.",
     [("    if len(vols) != n:", "    if vols and len(vols) != n:")]),
]

text = REF.read_text(encoding="utf-8")
close = text.index('"""', 3) + 3  # end of the reference's module docstring
body = text[close:]
for name, desc, edits in MUTANTS:
    mutant = body
    for old, new in edits:
        assert mutant.count(old) == 1, (name, old[:60], mutant.count(old))
        mutant = mutant.replace(old, new)
    (OUT / name).write_text(f'"""{desc}"""\n{mutant}', encoding="utf-8")
    print("wrote", name)
