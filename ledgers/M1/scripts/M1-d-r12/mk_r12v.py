"""Writes round-12 verifier student-error mutants r12v_01..r12v_04 of M1-d from the grader reference (run with python -I).
usage: mk_r12v.py <reference.py> <outdir>"""
import pathlib, sys
REF = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2])
src = REF.read_text(encoding="utf-8")
def rep(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)
muts = {
 "r12v_01_annuity_cutoff_1e-10_treated_as_zero.py": (
  "Annuity factor treats a rate below 1e-10 in size as zero and returns the number of periods, a cutoff the tests (rate 5e-10 only) do not reach.",
  rep(src, "    if r == 0:\n        return float(n)\n    return (1 - (1 + r) ** -n) / r",
      "    if abs(r) < 1e-10:\n        return float(n)\n    return (1 - (1 + r) ** -n) / r")),
 "r12v_02_annual_rate_read_as_binary_fraction.py": (
  "Exact arithmetic on the binary value of the float rate (Fraction(float)), not on the rate as it is written as a decimal.",
  rep(src, '    return Fraction(repr(annual_rate))', '    return Fraction(annual_rate)')),
 "r12v_03_schedule_interest_rounded_in_float.py": (
  "Schedule interest is computed in floating point, floor(opening * i + 0.5), not in exact rational arithmetic as the conventions require.",
  rep(src, "        interest = _nearest_cent(opening * i)",
      "        interest = math.floor(float(opening) * float(i) + 0.5)")),
 "r12v_04_growing_perpetuity_missing_upper_bound.py": (
  "Growing perpetuity drops the growth-below-rate check, so growth above the rate returns a negative value instead of being refused.",
  rep(src, '    if g >= r:\n        raise ValueError("growth must be below the rate: at growth at or above the rate the value is not finite")\n',
      "")),
}
for name, (doc, text) in muts.items():
    body = f'"""{doc}"""\n' + text.split('"""', 2)[2]
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)
