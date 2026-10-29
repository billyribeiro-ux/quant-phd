# Independent re-derivation of the L23 lab numbers with Decimal at 60 digits (no Fraction, no float money).
from decimal import Decimal as D, getcontext, ROUND_HALF_EVEN
getcontext().prec = 60
C = [D(5000)] * 9 + [D(105000)]
def v(y): return 1 + y
def P(y):
    b = v(y); return sum(C[t-1] / b**t for t in range(1, 11))
def P1(y):
    b = v(y); return -sum(t * C[t-1] / b**(t+1) for t in range(1, 11))
def P2(y):
    b = v(y); return sum(t*(t+1)*C[t-1] / b**(t+2) for t in range(1, 11))
y0 = D("0.04")
print("P(y0) =", P(y0).quantize(D("0.000001"), ROUND_HALF_EVEN))
print("int price", P(y0).quantize(D(1), ROUND_HALF_EVEN))
print("P1 =", P1(y0).quantize(D("0.000001")), "P2 =", P2(y0).quantize(D("0.000001")))
for dy in (D("0.01"), D("0.005"), D("0.0025")):
    ex = P(y0+dy); t1 = P(y0) + P1(y0)*dy; t2 = t1 + D("0.5")*P2(y0)*dy*dy
    print("dy", dy, "e1", "%.6e" % float(ex-t1), "e2", "%.6e" % float(ex-t2))
errs = []
for dy in (D("0.01"), D("0.005"), D("0.0025")):
    ex = P(y0+dy); t1 = P(y0) + P1(y0)*dy; t2 = t1 + D("0.5")*P2(y0)*dy*dy
    errs.append((ex-t1, ex-t2))
print("ratio1 k2", "%.6f" % float(errs[0][0]/errs[1][0]), "ratio1 k3", "%.6f" % float(errs[1][0]/errs[2][0]))
print("ratio2 k2", "%.6f" % float(errs[0][1]/errs[1][1]), "ratio2 k3", "%.6f" % float(errs[1][1]/errs[2][1]))
# cents at +0.01 and -0.01
for dy in (D("0.01"), D("-0.01")):
    ex = P(y0+dy); t2 = P(y0) + P1(y0)*dy + D("0.5")*P2(y0)*dy*dy
    print("shift", dy, "exact", ex.quantize(D(1), ROUND_HALF_EVEN), "second", t2.quantize(D(1), ROUND_HALF_EVEN), "diff", (ex.quantize(D(1), ROUND_HALF_EVEN) - t2.quantize(D(1), ROUND_HALF_EVEN)))
print("-P'/P", "%.6f" % float(-P1(y0)/P(y0)), "P''/P", "%.6f" % float(P2(y0)/P(y0)))
