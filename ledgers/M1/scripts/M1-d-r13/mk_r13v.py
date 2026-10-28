import pathlib, sys
ref = pathlib.Path("/tmp/verify13-M1-d/course/modules/M/M1/grader/reference.py").read_text()
out = pathlib.Path("/tmp/verify13-M1-d/ledgers/M1/mutants")
specs = {
 "r13v_01_monthly_rate_rounded_to_six_places.py": (
  "Level payment uses the monthly rate rounded to six decimal places, so the payment is off by more than a cent on a large loan.",
  "    i = _exact_rate(_annual_rate(annual_rate)) / 12\n    n = _months(months)\n    if i == 0:\n        return _nearest_cent(Fraction(principal, n))\n    return _nearest_cent(principal * i / (1 - (1 + i) ** -n))",
  "    i = _exact_rate(_annual_rate(annual_rate)) / 12\n    i = Fraction(round(float(i), 6))\n    n = _months(months)\n    if i == 0:\n        return _nearest_cent(Fraction(principal, n))\n    return _nearest_cent(principal * i / (1 - (1 + i) ** -n))"),
 "r13v_02_last_month_interest_truncated.py": (
  "Schedule takes the final month's interest down to whole cents (floor) while the other months use the nearest cent.",
  "        interest = _nearest_cent(opening * i)\n        paid = payment if period < n else opening + interest",
  "        interest = _nearest_cent(opening * i) if period < n else math.floor(opening * i)\n        paid = payment if period < n else opening + interest"),
 "r13v_03_level_payment_tiny_rate_cutoff_1e-9.py": (
  "Level payment treats any annual rate below 1e-9 as zero and returns the loan divided by the months, without the rate's effect.",
  "    if i == 0:\n        return _nearest_cent(Fraction(principal, n))",
  "    if i < Fraction(1, 10**9):\n        return _nearest_cent(Fraction(principal, n))"),
 "r13v_04_annuity_tiny_rate_cutoff_1e-12.py": (
  "Annuity factor treats a rate below 1e-12 in size as zero and returns the number of periods.",
  "    if r == 0:",
  "    if abs(r) < 1e-12:\n        return float(n)\n    if r == 0:"),
}
for name, (doc, old, new) in specs.items():
    assert ref.count(old) == 1, (name, ref.count(old))
    body = ref.replace(old, new, 1)
    # module docstring replaced by the one-line description the mutation tool reads
    first_end = body.index('"""', 3) + 3
    body = '"""' + doc + '"""' + body[first_end:]
    (out / name).write_text(body)
    print("wrote", name)
