import pathlib
ref = pathlib.Path('course/modules/M/M3/grader/reference.py').read_text()
head_end = ref.index('"""', 3) + 3  # end of the module docstring
body = ref[head_end:]
out = pathlib.Path('ledgers/M3/mutants')
specs = {
 'r9d_m01_clip_rebuilds_with_transposed_vectors.py': (
  'clip_repair rebuilds the clipped matrix from the transposed eigenvector matrix, so it computes V^T diag V.',
  "    x = _rebuild([max(value, floor) for value in values], vectors)\n",
  "    x = _rebuild([max(value, floor) for value in values], [list(row) for row in zip(*vectors, strict=True)])\n"),
 'r9d_m02_projection_returns_last_psd_iterate.py': (
  'projection_repair returns the last positive semidefinite projection, so its diagonal is not forced to 1.',
  "    return x\n\n\ndef comparison_weights",
  "    return y\n\n\ndef comparison_weights"),
 'r9d_m03_weights_scale_by_inverse_volatility.py': (
  'comparison_weights builds Sigma as S^-1 C S^-1 instead of S C S, so the weights use inverse volatilities.',
  "sigma = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]",
  "sigma = [[c[i][j] / (float(vols[i]) * float(vols[j])) for j in range(n)] for i in range(n)]"),
 'r9d_m04_is_psd_rejects_large_positive_eigenvalue.py': (
  'is_psd tests that the smallest eigenvalue lies within tol of zero, so a positive definite matrix with a large smallest eigenvalue is refused.',
  "    return min_eigenvalue(matrix) >= -tol\n",
  "    return abs(min_eigenvalue(matrix)) <= tol\n"),
 'r9d_m05_weights_normalised_by_first_entry.py': (
  'comparison_weights divides by the first solution component instead of the sum, so the weights do not sum to one.',
  "    total = sum(solution)\n",
  "    total = solution[0]\n"),
}
for name, (doc, old, new) in specs.items():
    assert body.count(old) == 1, name
    text = body.replace(old, new)
    (out / name).write_text(f'"""{doc}"""\n' + text)
    print('wrote', name)
