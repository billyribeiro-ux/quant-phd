"""M2-d2 r10: independent recomputation of L24 numbers (Decimal at 60 digits for exact values; float for printed).

Exact central error of exp at 1 with step h is e*(sinh(h)/h - 1); exact forward error is e*((e^h - 1)/h - 1).
"""
from decimal import Decimal as D, getcontext
import math
getcontext().prec = 60
e = D(1).exp()
def exact_fwd(h):
    h = D(h)
    return e * ((h.exp() - 1) / h - 1)
def exact_cen(h):
    h = D(h)
    return e * ((h.exp() - (-h).exp()) / (2 * h) - 1)
print("exact forward error h=1e-8: %.4e" % float(exact_fwd("1e-8")))
for h in ["1e-4", "1e-5", "1e-6", "1e-7"]:
    print("exact central error h=%s: %.4e" % (h, float(exact_cen(h))))
print("exact central/ ratio 1e-4 to 1e-5 (exact):", float(exact_cen("1e-4") / exact_cen("1e-5")))
print("printed ratio 4.531e-9/5.859e-11 =", 4.531e-9 / 5.859e-11)
# float (as the lab computes) unrounded central quotient errors
E = math.exp(1.0)
for h in [1e-5, 1e-7]:
    q = (math.exp(1.0 + h) - math.exp(1.0 - h)) / (2 * h)
    print("float central quotient h=%g: error %.9e" % (h, abs(q - E)))
qa = (math.exp(1.0 + 1e-5) - math.exp(1.0 - 1e-5)) / (2e-5)
qb = (math.exp(1.0 + 1e-7) - math.exp(1.0 - 1e-7)) / (2e-7)
print("unrounded difference of the two float errors:", abs(qb - E) - abs(qa - E), "abs-diff", abs(abs(qa - E) - abs(qb - E)))
delta = 2.0 ** -52
print("delta = 2^-52 = %.3e" % delta, " 2*sqrt(delta/e) = %.3e" % (2 * math.sqrt(delta / E)), " (3 delta/e)^(1/3) = %.3e" % ((3 * delta / E) ** (1 / 3)))
print("round-off bound 2 delta/h at h=1e-15: %.3f" % (2 * delta / 1e-15))
print("grid spacing 2.2e-16/h at h=1e-15 -> 2.2e-16/1e-15 = %.3f" % (2.2e-16 / 1e-15))
print("floats near e: ulp(e) = %.3e, half ulp = %.3e" % (math.ulp(E), math.ulp(E) / 2))
# signed computed forward error at h = 1e-8 (lesson L24.html:129 says -6.603e-9; the lab prints only its absolute value)
Ef = math.exp(1.0)
sq = (math.exp(1.0 + 1e-8) - Ef) / 1e-8
print("signed float forward error h=1e-8: %.4e" % (sq - Ef))
