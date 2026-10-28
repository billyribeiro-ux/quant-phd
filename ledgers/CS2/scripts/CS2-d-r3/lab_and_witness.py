"""Verifier round 3: independent recomputation of Lab 3 numbers and the float rank-target witness."""
import math
from fractions import Fraction

S = ["10003.2","10001.7","10007.5","10000.4","10004.9","10002.1","10009.6","10001.0","10006.3","10003.8","10005.5"]
ex = [Fraction(s) for s in S]
n = len(ex)
m = sum(ex) / n
v = sum((x - m) ** 2 for x in ex) / (n - 1)
print("sum", float(sum(ex)), "exact mean", float(m), "exact var", float(v))
print("var rounded 6dp", f"{float(v):.6f}", "exact var unrounded", v.numerator / v.denominator)
print("last4 min/max", min(S[-4:]), max(S[-4:]))
qn = Fraction(1, 2) * n
en = Fraction(1, 10) * n
print("qn-en", float(qn - en), "ceil", math.ceil(qn - en))
# float witness
print("float 0.1*20-0.05*20 =", 0.1 * 20 - 0.05 * 20, "ceil", math.ceil(0.1 * 20 - 0.05 * 20))
ex_t = Fraction(0.1) * 20 - Fraction(0.05) * 20
print("exact diff", float(ex_t), "exact diff minus 1 =", float(ex_t - 1), "ceil", math.ceil(ex_t))
print("exact diff digits", f"{float(ex_t - 1):.20e}")
# count of witness cases quoted in the grader? list n<=20 small cases
