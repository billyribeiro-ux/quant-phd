from decimal import Decimal as D, getcontext
getcontext().prec = 60
a, s, d, n = D("0.3"), D("0.2"), D("0.05"), D("0.01")
ks = (s / (n + d)) ** (1 / (1 - a))
print("k*", f"{ks:.10f}", "y*", f"{ks ** a:.10f}")
print("dk/ds", f"{ks / ((1 - a) * s):.10f}", "dk/dd", f"{-ks / ((1 - a) * (n + d)):.10f}")
k = D(1); first = None
for t in range(1, 1001):
    k = (s * k ** a + (1 - d) * k) / (1 + n)
    gap = abs(k - ks)
    if t in (50, 100): print("period", t, f"{k:.10f}", f"{gap:.10f}")
    if first is None and gap < D("1e-12"): first = t
print("first_gap_below_1e-12", first)
