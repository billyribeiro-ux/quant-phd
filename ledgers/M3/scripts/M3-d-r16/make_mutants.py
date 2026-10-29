import sys
ref = open(sys.argv[1], encoding="utf-8").read()
out = sys.argv[2]
muts = {
 "r16d_m01_is_psd_tolerance_scaled_by_spectrum.py": (
  "return min_eigenvalue(matrix) >= -tol\n",
  "return min_eigenvalue(matrix) >= -tol * max(1.0, max(abs(v) for v in _eigh(_as_matrix(matrix))[0]))\n",
  '"""is_psd scales the tolerance by the largest absolute eigenvalue, so it is looser for large matrices."""\n'),
 "r16d_m02_min_eigenvalue_prints_its_value.py": (
  "    values, _ = _eigh(_as_matrix(matrix))\n    return min(values)\n",
  "    values, _ = _eigh(_as_matrix(matrix))\n    print('smallest eigenvalue:', min(values))\n    return min(values)\n",
  '"""min_eigenvalue prints its result as a debugging aid, which the specification forbids."""\n'),
 "r16d_m03_clip_repair_writes_back_into_argument.py": (
  "    return _rescale(x)\n\n\ndef projection_repair",
  "    out = _rescale(x)\n    for i in range(len(matrix)):\n        matrix[i][:] = out[i]\n    return out\n\n\ndef projection_repair",
  '"""clip_repair overwrites the caller matrix with the repaired values, changing its argument."""\n'),
}
for name, (old, new, doc) in muts.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new, 1)
    # replace module docstring line 1-? : prepend a one-line docstring is not allowed twice; swap the first docstring
    first_end = body.index('"""', 3) + 3
    body = doc.strip() and (doc.strip()[:0]) + body
    body = body[:body.index('"""')] + doc.strip() + body[first_end:]
    open(out + "/" + name, "w", encoding="utf-8").write(body)
    print("wrote", name)
