import re
ref = open("course/modules/M/M4/grader/reference.py", encoding="utf-8").read()
end = ref.index('"""', 3) + 3  # close of module docstring
body = ref[end:]
M = "ledgers/M4/mutants/"
specs = {
 "r13_01_loss_rounded_per_position.py": (
  "Verifier round-13 student-error mutant. Each position's loss is rounded to a whole cent before the sum, not the portfolio loss once.",
  [("        total = 0.0\n        for i in range(n):\n            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))\n            total += position_cents[i] * ret\n        losses.append(round(-total))",
    "        total = 0\n        for i in range(n):\n            ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))\n            total += round(-position_cents[i] * ret)\n        losses.append(total)")]),
 "r13_02_quantile_index_floor_not_ceiling.py": (
  "Verifier round-13 student-error mutant. The 99% index is floor(0.99 n) instead of ceil(0.99 n), one order statistic high at n = 101.",
  [("index = (99 * len(losses_cents) + 99) // 100", "index = (99 * len(losses_cents)) // 100")]),
 "r13_03_matched_scale_inverted_chi_square.py": (
  "Verifier round-13 student-error mutant. The Student-t scale divides by nu instead of the chi-square draw, so each draw's scale is sqrt(matched * nu / nu) times the wrong factor.",
  [("scale = math.sqrt(matched * nu / chi_square)", "scale = math.sqrt(matched * chi_square / nu)")]),
 "r13_04_cholesky_transposed_in_returns.py": (
  "Verifier round-13 student-error mutant. The return for position i uses column i of L (the transpose), so the cross term has the wrong dependence.",
  [("ret = scale * sum(factor[i][k] * z[k] for k in range(i + 1))", "ret = scale * sum(factor[k][i] * z[k] for k in range(i, n))")]),
}
for name, (doc, reps) in specs.items():
    b = body
    for old, new in reps:
        assert b.count(old) == 1, (name, b.count(old))
        b = b.replace(old, new)
    open(M + name, "w", encoding="utf-8").write(f'"""{doc}"""' + b)
    print("wrote", name)
