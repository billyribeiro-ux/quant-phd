# Independent recomputation of the L23 printed numbers, with mpmath-free Decimal at 50 digits (not the twin's code).
# Usage: python -I recheck_L23_numbers.py
from decimal import Decimal as D, getcontext, ROUND_HALF_EVEN
getcontext().prec = 60
c = [D(5000)] * 9 + [D(105000)]  # c_1..c_10
def P(y):
    return sum(c[t - 1] / (1 + y) ** t for t in range(1, 11))
def Pp(y):
    return -sum(t * c[t - 1] / (1 + y) ** (t + 1) for t in range(1, 11))
def Ppp(y):
    return sum(t * (t + 1) * c[t - 1] / (1 + y) ** (t + 2) for t in range(1, 11))
def Pppp(y):
    return -sum(t * (t + 1) * (t + 2) * c[t - 1] / (1 + y) ** (t + 3) for t in range(1, 11))
y0 = D("0.04")
print("unrounded P(0.04) =", P(y0).quantize(D("0.000001")), "rounded half-even =", P(y0).quantize(D("1"), ROUND_HALF_EVEN))
print("P'(0.04) =", Pp(y0).quantize(D("0.000001")), "P''(0.04) =", Ppp(y0).quantize(D("0.000001")))
print("-P'/P =", (-Pp(y0) / P(y0)).quantize(D("0.000001")), " P''/P =", (Ppp(y0) / P(y0)).quantize(D("0.000001")))
def T1(dy): return P(y0) + Pp(y0) * dy
def T2(dy): return T1(dy) + Ppp(y0) * dy * dy / 2
for dy in (D("0.01"), D("0.005"), D("0.0025")):
    e1 = P(y0 + dy) - T1(dy)
    e2 = P(y0 + dy) - T2(dy)
    print("dy", dy, "e1", e1.quantize(D("0.0001")), "e2", e2.quantize(D("0.0001")), "e1 %.6e" % float(e1), "e2 %.6e" % float(e2))
print("e1 ratio 0.01/0.005 =", float((P(y0+D('0.01'))-T1(D('0.01')))/(P(y0+D('0.005'))-T1(D('0.005')))))
print("e2 ratio 0.01/0.005 =", float((P(y0+D('0.01'))-T2(D('0.01')))/(P(y0+D('0.005'))-T2(D('0.005')))))
print("e1 ratio 0.005/0.0025 =", float((P(y0+D('0.005'))-T1(D('0.005')))/(P(y0+D('0.0025'))-T1(D('0.0025')))))
print("e2 ratio 0.005/0.0025 =", float((P(y0+D('0.005'))-T2(D('0.005')))/(P(y0+D('0.0025'))-T2(D('0.0025')))))
for dy in (D("0.01"), D("-0.01")):
    ex = P(y0 + dy); ap = T2(dy)
    print("shift", dy, "exact", ex.quantize(D("0.000001")), "T2", ap.quantize(D("0.000001")), "exact-T2 =", (ex - ap).quantize(D("0.000001")))
print("P''' sign check at 0.04:", Pppp(y0) < 0)
# finite-difference check of P' and P'' with h = 1e-5 and 1e-4 (Decimal)
h = D("1e-5")
print("central diff P' h=1e-5:", ((P(y0 + h) - P(y0 - h)) / (2 * h)).quantize(D("0.000001")))
h2 = D("1e-4")
print("central diff P'' via P' h=1e-4:", ((Pp(y0 + h2) - Pp(y0 - h2)) / (2 * h2)).quantize(D("0.000001")))
