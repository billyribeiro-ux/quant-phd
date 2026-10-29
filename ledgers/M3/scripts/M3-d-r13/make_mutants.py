import sys, pathlib
ref = pathlib.Path("course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
M = pathlib.Path("ledgers/M3/mutants")
specs = {
 "r13d_m01_clip_floor_applied_only_when_positive.py": (
  "clip_repair ignores the floor when it is zero, so negative eigenvalues survive the clip at floor 0 and the repair is not PSD.",
  "    x = _rebuild([max(value, floor) for value in values], vectors)",
  "    x = _rebuild([max(value, floor) if floor > 0.0 else value for value in values], vectors)"),
 "r13d_m02_weights_skip_pivot_division.py": (
  "comparison_weights reads the solution as the augmented column without dividing by the pivot, so it solves only when Sigma is the identity.",
  "    solution = [aug[i][n] / aug[i][i] for i in range(n)]",
  "    solution = [aug[i][n] for i in range(n)]"),
 "r13d_m03_projection_unit_diagonal_correction_sign_flipped.py": (
  "projection_repair's Dykstra correction for the unit-diagonal set has the wrong sign, so the iteration does not project onto that set.",
  "        corr_u = [[y[i][j] + corr_u[i][j] - new_x[i][j] for j in range(n)] for i in range(n)]",
  "        corr_u = [[new_x[i][j] - y[i][j] - corr_u[i][j] for j in range(n)] for i in range(n)]"),
 "r13d_m04_weights_off_diagonal_volatility_dropped.py": (
  "comparison_weights builds Sigma with the volatilities on the diagonal only, so Sigma is not S C S when the off-diagonal entries are nonzero.",
  "    sigma = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]",
  "    sigma = [[(float(vols[i]) ** 2 if i == j else c[i][j]) for j in range(n)] for i in range(n)]"),
 "r13d_m05_min_eigenvalue_last_jacobi_value.py": (
  "min_eigenvalue returns the last Jacobi diagonal entry instead of the minimum, which is right only when the last entry is the smallest.",
  "    values, _ = _eigh(_as_matrix(matrix))\n    return min(values)",
  "    values, _ = _eigh(_as_matrix(matrix))\n    return values[-1]"),
}
for name, (doc, old, new) in specs.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new)
    # replace the module docstring (first triple-quoted block) with the one-line description
    start = body.index('"""'); end = body.index('"""', start + 3) + 3
    body = '"""' + doc + '"""' + body[end:]
    (M / name).write_text(body, encoding="utf-8")
    print("wrote", name)
