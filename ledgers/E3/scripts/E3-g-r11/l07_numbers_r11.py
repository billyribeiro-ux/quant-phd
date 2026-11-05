"""Re-derive the L07 numbers (Example 1.4, Remark 1.6, Prop 2.2, E2, misconception, E1 crossing, M1, E3 alt eta) with decimal at 60 digits."""
from decimal import Decimal as D, getcontext
import math
getcontext().prec = 60

def om(p):  # closed form eta=1/2
    p = D(p)
    return p.sqrt() / (1 + 2 * (p * (1 - p)).sqrt())

def om_general(p, eta=D("0.5")):
    p = D(p)
    return (p ** eta) / ((p ** eta + (1 - p) ** eta) ** (1 / eta))

print("omega(3/10) =", om(D(3) / 10))
print("omega(3/5)  =", om(D(3) / 5))
print("omega(1/2)  =", om(D("0.5")), " 1/(2 sqrt2) =", 1 / (2 * D(2).sqrt()))
print("omega(2/5)  =", om(D(2) / 5))
print("omega(1/4)  =", om(D("0.25")), " 2-sqrt3 =", 2 - D(3).sqrt())
print("omega(0.01) =", om(D("0.01")), " omega(0.99) =", om(D("0.99")))
print("sum weights A = omega(2/5)+2 omega(3/10) =", om(D(2) / 5) + 2 * om(D(3) / 10))
print("2 omega(3/10) =", 2 * om(D(3) / 10), " 2omega(3/10)/omega(3/5) ratio:", om(D(3) / 10) / om(D(3) / 5))
ratio = om(D(3) / 10) / om(D(3) / 5)
print("ratio 8dp (Decimal quantize):", ratio.quantize(D("0.00000001")))
print("ratio vs 0.73045450 diff:", ratio - D("0.73045450"))
print("1/(1+2^-1)=", 1 / (1 + D(2) ** -1), " 1/(1+2^-1/2)=", 1 / (1 + D(2) ** D("-0.5")))
# Gamma values at alpha=1
GA = 150 * om(D(3) / 10)
GB = 100 * om(D(3) / 5)
print("Gamma(A) alpha=1 =", GA)
print("Gamma(B) alpha=1 =", GB)
print("difference 40-digit =", GA - GB, " to 4dp:", (GA - GB).quantize(D("0.0001")))
print("8dp roundings:", GA.quantize(D("0.00000001")), GB.quantize(D("0.00000001")),
      "difference of 8dp:", GA.quantize(D("0.00000001")) - GB.quantize(D("0.00000001")))
print("printed difference 42.8686-39.1251 =", D("42.8686") - D("39.1251"))
# alpha = 1/2
GA5 = om(D(3) / 10) * (D(50).sqrt() + D(100).sqrt())
GB5 = om(D(3) / 5) * D(10)
print("alpha=1/2 Gamma(A)=", GA5, " Gamma(B)=", GB5)
# misconception: L = 100 w.p. 0.01, 50 w.p. 0.99
w1 = om(D("0.01")); w99 = om(D("0.99"))
WL = w1 * 100 + w99 * 50
print("weighted L =", WL, " EV =", D("0.01") * 100 + D("0.99") * 50)
print("overweight term", (w1 - D("0.01")) * 100, " underweight term", (D("0.99") - w99) * 50, " net", (w1 - D("0.01")) * 100 - (D("0.99") - w99) * 50)
# Example 1.4 derivative formula check numerically (float central difference)
def omf(p):
    return math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))
def deriv_formula(p):
    q = math.sqrt(p * (1 - p))
    return (q + 2 * p * p) / (2 * math.sqrt(p) * q * (1 + 2 * q) ** 2)
for p in (0.01, 0.1, 0.3, 0.5, 0.7, 0.99):
    h = 1e-7
    num = (omf(p + h) - omf(p - h)) / (2 * h)
    print(f"p={p}: numeric {num:.10f} formula {deriv_formula(p):.10f}")
# crossing near 0.278
grid = [i / 1000 for i in range(1001)]
above = [p for p in grid[1:-1] if omf(p) > p]
print("last grid point with omega>p:", max(above), " omega(0.278)-0.278 =", omf(0.278) - 0.278, " omega(0.279)-0.279 =", omf(0.279) - 0.279)
# exact crossing by bisection
lo, hi = 0.278, 0.279
for _ in range(60):
    mid = (lo + hi) / 2
    if omf(mid) > mid:
        lo = mid
    else:
        hi = mid
print("crossing ~", lo)
# unrounded at 10 dp
print("10dp:", f"{float(om(D(3)/10)):.10f}", f"{float(om(D(3)/5)):.10f}", f"{float(om(D('0.5'))):.10f}")
