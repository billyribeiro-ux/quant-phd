import pathlib
ref = pathlib.Path('course/modules/M/M3/grader/reference.py').read_text(encoding='utf-8')
out = pathlib.Path('ledgers/M3/mutants')
specs = {
 'r6d_m01_clip_sorts_values_not_vectors.py': (
  'clip_repair sorts the eigenvalues ascending but rebuilds from the unsorted eigenvectors, so the vectors no longer match their eigenvalues.',
  '    values, vectors = _eigh(a)\n    x = _rebuild([max(value, floor) for value in values], vectors)',
  '    values, vectors = _eigh(a)\n    values = sorted(values)\n    x = _rebuild([max(value, floor) for value in values], vectors)'),
 'r6d_m02_comparison_sigma_row_scaled_twice.py': (
  'comparison_weights builds Sigma with vols[i] on both sides of C (Sigma_ij = v_i C_ij v_i), which is not symmetric and not D C D.',
  '    sigma = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]',
  '    sigma = [[float(vols[i]) * c[i][j] * float(vols[i]) for j in range(n)] for i in range(n)]'),
 'r6d_m03_symmetry_check_skips_last_column_pair.py': (
  '_as_matrix checks the symmetry of the pairs (i, j) with j below n-1 only, so an asymmetry in the last column is accepted.',
  '        for j in range(i + 1, n):\n            if abs(out[i][j] - out[j][i]) > SYMMETRY_TOL:',
  '        for j in range(i + 1, n - 1):\n            if abs(out[i][j] - out[j][i]) > SYMMETRY_TOL:'),
 'r6d_m04_projection_stops_on_gap_only.py': (
  'projection_repair stops when the gap alone is at most tol, and ignores the step, so it can stop before the iterate has settled.',
  '        if gap <= tol and step <= tol:\n            break',
  '        if gap <= tol:\n            break'),
}
for name,(doc,old,new) in specs.items():
    assert ref.count(old)==1, name
    body = ref.replace(old,new)
    body = body.replace('"""Reference solution for the M3 project, covariance_doctor.py. Not shipped to learners.', '"""'+doc+'\n\nMutant of the reference. Not shipped to learners.',1)
    (out/name).write_text(body, encoding='utf-8')
    print('wrote', name)
