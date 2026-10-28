import sys
REF = "/tmp/verify8-M1-d/course/modules/M/M1/grader/reference.py"
OUT = "/tmp/verify8-M1-d/ledgers/M1/mutants/"
src = open(REF, encoding="utf-8").read()
head, rest = src.split('"""', 2)[1], src.split('"""', 2)[2]
def make(name, desc, old, new, count=1):
    body = src.replace(old, new, count)
    assert body != src, name
    body = body.replace('"""Reference solution for the M1 project', '"""' + desc + '\n\nReference solution for the M1 project', 1)
    open(OUT + name, "w", encoding="utf-8").write(body)
make("m47_schedule_omits_the_last_month.py",
     "Schedule error: the schedule returns months 1 to n-1 only, so the last row (the one that clears the balance) is missing.",
     "for period in range(1, n + 1):", "for period in range(1, n):")
make("m48_small_rate_cutoff_loan_over_months.py",
     "Numerical cutoff: a rate below 1e-6 a year is taken as zero, so the level payment is the loan over the months, not the annuity payment.",
     "    if i == 0:\n        return _nearest_cent(Fraction(principal, n))",
     "    if i < Fraction(1, 10**6) / 12:\n        return _nearest_cent(Fraction(principal, n))\n    if i == 0:\n        return _nearest_cent(Fraction(principal, n))")
make("m49_interest_on_original_principal.py",
     "Schedule error: each month's interest is charged on the original loan, not on the opening balance of that month.",
     "interest = _nearest_cent(opening * i)", "interest = _nearest_cent(principal * i)")
make("m50_perpetuity_rejects_rate_of_one_or_more.py",
     "Over-tight guard: the perpetuity factor refuses any rate of one or more (100 % a period), although a positive rate is all the specification requires.",
     "    if r <= 0:\n        raise ValueError(\"a perpetuity needs",
     "    if r <= 0 or r >= 1:\n        raise ValueError(\"a perpetuity needs")
print("ok")
