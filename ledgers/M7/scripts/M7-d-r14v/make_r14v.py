import sys
R = sys.argv[1]; M = sys.argv[2]; S = sys.argv[3]
src = open(R, encoding="utf-8").read()
def rep(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)
# new student-error mutants (verifier, round 14)
m1 = rep(src, "    for signs in product((1, -1), repeat=n):\n        a = [Fraction(s) for s in signs]\n        rows.append((a, problem.tau + _dot(a, problem.w0), (\"turn\", signs)))",
          "    for signs in product((1, -1), repeat=n):\n        a = [Fraction(s) for s in signs]\n        rows.append((a, problem.tau + Fraction(1, 10**7) + _dot(a, problem.w0), (\"turn\", signs)))")
m1 = '"""Student error v14_01: the turnover sign forms are relaxed by 1e-7, so the turnover limit is exceeded by up to 1e-7."""\n' + m1
m2 = rep(src, "            working.pop(min(negative)[1])\n            continue",
          "            return x, {rows[j][2]: lam[1 + k] for k, j in enumerate(working)}, lam[0]\n            working.pop(min(negative)[1])\n            continue")
m2 = '"""Student error v14_02: the active-set search returns at the first KKT step even when a working multiplier is negative, so dual feasibility is not enforced."""\n' + m2
m3 = rep(src, "    return {\n        \"w\": x,\n        \"budget\": budget_mult,",
          "    return {\n        \"w\": x,\n        \"budget\": budget_mult * problem.gamma,\n        \"_unused\": 0,\n        \"budget_raw\": budget_mult,")
m3 = '"""Student error v14_03: the budget multiplier reported is scaled by gamma, which is wrong for gamma other than one."""\n' + m3
for name, text in (("v14_01_turnover_limit_relaxed_by_1e-7.py", m1), ("v14_02_negative_multiplier_not_removed.py", m2), ("v14_03_budget_multiplier_scaled_by_gamma.py", m3)):
    open(f"{M}/{name}", "w", encoding="utf-8").write(text)
# alternative correct implementations
a1 = rep(src, "    for j, (a, b, _) in enumerate(rows):\n        if b - _dot(a, x) <= TOL", "    for j, (a, b, _) in reversed(list(enumerate(rows))):\n        if b - _dot(a, x) <= TOL")
open(f"{S}/alt_reversed_rows_r14v.py", "w", encoding="utf-8").write(a1)
a2 = rep(src, "            working.pop(min(negative)[1])", "            working.pop(min(negative, key=lambda item: (item[0], -item[1]))[1])")
open(f"{S}/alt_most_negative_pop_r14v.py", "w", encoding="utf-8").write(a2)
print("ok")
