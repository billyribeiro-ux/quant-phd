import pathlib
ref = pathlib.Path("course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
# strip the reference's multi-line module docstring; each mutant opens with its own one-line docstring
end = ref.index('"""', 3) + 3
body_src = ref[end:]
out = pathlib.Path("ledgers/M3/mutants")
muts = {
 "r10d_m01_weights_offdiagonal_unscaled": (
  "comparison_weights scales only the diagonal of C by the volatilities, so the off-diagonal covariances ignore them.",
  "    sigma = [[float(vols[i]) * c[i][j] * float(vols[j]) for j in range(n)] for i in range(n)]",
  "    sigma = [[float(vols[i]) ** 2 if i == j else c[i][j] for j in range(n)] for i in range(n)]"),
 "r10d_m02_rescale_divides_by_own_diagonal": (
  "_rescale divides entry (i, j) by d_i alone, so the result is not symmetric and its diagonal is not one.",
  "    return [[x[i][j] / math.sqrt(d[i] * d[j]) for j in range(len(x))] for i in range(len(x))]",
  "    return [[x[i][j] / d[i] for j in range(len(x))] for i in range(len(x))]"),
 "r10d_m03_dykstra_never_updates_unit_correction": (
  "projection_repair never updates the unit-diagonal correction, so the iteration is not Dykstra's and can stop short of the nearest matrix.",
  "        corr_u = [[y[i][j] + corr_u[i][j] - new_x[i][j] for j in range(n)] for i in range(n)]",
  "        corr_u = corr_u"),
}
for name, (doc, old, new) in muts.items():
    assert body_src.count(old) == 1, (name, body_src.count(old))
    body = '"""' + doc + '"""\n' + body_src.replace(old, new)
    (out / f"{name}.py").write_text(body, encoding="utf-8")
    print("wrote", name)
