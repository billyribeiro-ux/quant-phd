import pathlib, re
ref = pathlib.Path("/tmp/verifyB3-M4-d/course/modules/M/M4/grader/reference.py").read_text()
out_m = pathlib.Path("/tmp/verifyB3-M4-d/ledgers/M4/mutants")
out_s = pathlib.Path("/tmp/M4-v/d/scratch")
def rep(src, old, new):
    assert src.count(old) == 1, old
    return src.replace(old, new)
mutants = {
 "v3_m01_quantile_float_index.py": ('"""Verifier round-3 student-error mutant. The 99% index is computed as math.ceil(0.99 * n) in floating point, which overshoots by one order statistic when 0.99 * n is a whole number above its float value (n = 100).\n"""\n',
   ("    index = (99 * len(losses_cents) + 99) // 100\n", "    index = math.ceil(0.99 * len(losses_cents))\n")),
 "v3_m02_round_half_up_by_truncation.py": ('"""Verifier round-3 student-error mutant. Losses are rounded with int(x + 0.5) instead of round(), which rounds a negative loss toward zero half a cent too high.\n"""\n',
   ("        losses.append(round(-total))\n", "        losses.append(int(-total + 0.5))\n")),
 "v3_m03_loss_scaled_by_weights.py": ('"""Verifier round-3 student-error mutant. Each position is divided by the total portfolio value before the loss is formed, so the loss is a fraction of a cent-valued weight, not cents.\n"""\n',
   ("            total += position_cents[i] * ret\n", "            total += position_cents[i] / sum(position_cents) * ret\n")),
}
for name, (doc, (old, new)) in mutants.items():
    body = rep(ref, ref.split('"""', 2)[0] + '"""' + ref.split('"""', 2)[1] + '"""\n', "") if False else ref
    # replace module docstring (first triple-quoted block) with the mutant description
    head, rest = body.split('"""', 1)
    _, rest = rest.split('"""', 1)
    body = doc + rest.lstrip("\n")
    body = rep(body, old, new)
    (out_m / name).write_text(body)
    (out_s / name).write_text(body)
# alternatives (correct): written to scratch
alts = {
 "altA_chisq_sum_of_squares.py": [("            chi_square = rng.gammavariate(nu / 2, 2.0)\n",
    "            chi_square = sum(rng.gauss(0.0, 1.0) ** 2 for _ in range(nu))\n")],
 "altB_ceil_by_integer_division_float.py": [("    index = (99 * len(losses_cents) + 99) // 100\n",
    "    index = math.ceil(len(losses_cents) * 99 / 100)\n")],
 "altC_crout_cholesky_column_order.py": [],
}
for name, reps in alts.items():
    body = ref
    for old, new in reps:
        body = rep(body, old, new)
    (out_s / name).write_text(body)
print("ok")
