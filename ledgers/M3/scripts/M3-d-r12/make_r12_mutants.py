import pathlib, sys
R = pathlib.Path(sys.argv[1])
ref = (R / "course/modules/M/M3/grader/reference.py").read_text()
out = R / "ledgers/M3/mutants"
specs = {
  "r12d_m02_min_eigenvalue_first_jacobi_value": (
    "    values, _ = _eigh(_as_matrix(matrix))\n    return min(values)",
    "    values, _ = _eigh(_as_matrix(matrix))\n    return values[0]",
    "min_eigenvalue returns the first eigenvalue Jacobi produces, not the smallest one, so a planted matrix whose first Jacobi value is not the minimum reports the wrong smallest eigenvalue.",
  ),
  "r12d_m03_projection_keeps_negatives_down_to_minus_0p01": (
    "    return _rebuild([max(x, 0.0) for x in values], vectors)",
    "    return _rebuild([max(x, -0.01) for x in values], vectors)",
    "_psd_projection floors eigenvalues at -0.01 instead of 0, so the repaired matrix keeps negative eigenvalues and is not positive semidefinite.",
  ),
  "r12d_m04_weights_scale_row_by_first_volatility": (
    "    sigma = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]",
    "    sigma = [[float(vols[i]) * c[i][j] * float(vols[i]) for j in range(n)] for i in range(n)]",
    "comparison_weights scales the covariance entry (i, j) by vols[i] twice, so Sigma is not S C S and the weights are wrong whenever the volatilities differ.",
  ),
}
for name, (old, new, desc) in specs.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new)
    head, sep, rest = body.partition('"""')
    body = '"""' + desc + '"""' + rest.split('"""', 1)[1] if False else body
    body = f'"""{desc}"""\n' + body
    (out / f"{name}.py").write_text(body)
    print("wrote", name)
