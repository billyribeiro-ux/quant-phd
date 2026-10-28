import pathlib
ref = pathlib.Path("/tmp/verify13-M1-d/course/modules/M/M1/grader/reference.py").read_text()
old_af = "    if r == 0:\n        return float(n)\n    return (1 - (1 + r) ** -n) / r"
assert ref.count(old_af) == 1
alts = {
 # a: valid algorithm, direct summation for moderate n, closed form beyond; zero rate exact
 "alt_r13_a_direct_sum_annuity.py": ref.replace(old_af,
   "    if r == 0:\n        return float(n)\n    if n <= 200_000:\n        v = 1 / (1 + r)\n        total, term = 0.0, 1.0\n        for _ in range(n):\n            term *= v\n            total += term\n        return total\n    return (1 - (1 + r) ** -n) / r"),
 # b: different cutoff (zero only below 1e-14) and log1p/expm1 closed form, a valid numerical method
 "alt_r13_b_expm1_cutoff_1e-14.py": ref.replace(old_af,
   "    import math as _m\n    if abs(r) < 1e-14:\n        return float(n)\n    return -_m.expm1(-n * _m.log1p(r)) / r"),
 # c: Horner-free recurrence on the factor a_n = (1 - v * a_{n-1}...) via closed form with division by r computed as (1 - v^n)/r with v^n via pow of float reciprocal
 "alt_r13_c_reciprocal_power_annuity.py": ref.replace(old_af,
   "    if r == 0:\n        return float(n)\n    v = 1.0 / (1.0 + r)\n    return (1.0 - v ** n) / r"),
}
for name, body in alts.items():
    pathlib.Path("/tmp/m1-v13/d/alts", name).write_text(body)
    print("wrote", name)
