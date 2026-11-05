import pathlib
root = pathlib.Path(".")
twin = (root / "tests/labs/LX2/lab-LX2-project-2.py").read_text(encoding="utf-8")
doc_end = twin.index('"""', 3) + 3
body = twin[doc_end:]
muts = {
 "r9_lab2_bias_negated_when_error_sum_positive.py": (
  "Student error (sign convention): the bias is negated whenever the error sum is positive, so an over-forecast prints as an under-forecast.",
  "    bias = Fraction(sum(errors), horizon)", "    bias = Fraction(-sum(errors), horizon) if sum(errors) > 0 else Fraction(sum(errors), horizon)"),
 "r9_lab2_edge_list_tests_one_unit.py": (
  "Student error (edge months): Part D lists the months with |error| = 1 instead of |error| = 2.",
  "if abs(e) == HIT_BAND]", "if abs(e) == HIT_BAND - 1]"),
 "r9_lab2_hit_band_half_open_upper.py": (
  "Student error (band): the hit test is half-open, -2 <= error < 2, so a month at +2 exactly is a miss.",
  "    return abs(predicted - realised) <= HIT_BAND", "    return -HIT_BAND <= predicted - realised < HIT_BAND"),
 "r9_lab2_bias_mean_of_squared_errors.py": (
  "Student error (definition): the bias is the mean of the squared errors, not the mean signed error.",
  "    bias = Fraction(sum(errors), horizon)", "    bias = Fraction(sum(e * e for e in errors), horizon)"),
}
for name, (doc, old, new) in muts.items():
    text = '"""' + doc + '"""' + body
    if old not in text: raise SystemExit(f"anchor missing for {name}: {old!r}")
    text = text.replace(old, new, 1)
    (root / "ledgers/LX2/mutants" / name).write_text(text, encoding="utf-8")
    print("wrote", name)
