import pathlib
ref = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB17-M3-d/course/modules/M/M3/grader/reference.py").read_text(encoding="utf-8")
out = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyB17-M3-d/ledgers/M3/mutants")
muts = {
 "r17d_m01_comparison_weights_normalised_by_largest_entry.py": (
  "comparison_weights normalises by the largest solution entry instead of by the sum, so the weights do not sum to one.",
  "    total = sum(solution)\n", "    total = max(solution)\n"),
 "r17d_m02_projection_repair_ignores_max_iter_argument.py": (
  "projection_repair hard-codes 500 iterations and ignores its max_iter argument.",
  "    for _ in range(max_iter):\n        y = _psd_projection", "    for _ in range(500):\n        y = _psd_projection"),
 "r17d_m03_rescale_divides_only_by_row_diagonal.py": (
  "_rescale divides entry (i, j) by the square root of the diagonal of row i alone, so the result is not symmetric.",
  "[[x[i][j] / math.sqrt(d[i] * d[j]) for j in range(len(x))] for i in range(len(x))]",
  "[[x[i][j] / math.sqrt(d[i]) for j in range(len(x))] for i in range(len(x))]"),
}
for name, (doc, old, new) in muts.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new, 1)
    lines = body.split("\n", 1)
    # replace the module docstring (first line of the file) with the one-line error description
    head_end = body.index('"""', 3) + 3
    body = '"""' + doc + '"""' + body[head_end:]
    (out / name).write_text(body, encoding="utf-8")
    print("wrote", name)
