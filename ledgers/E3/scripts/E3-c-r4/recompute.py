"""Round 4: independent recomputation of every number on L07 and L08 (floats and exact fractions)."""
import math
from fractions import Fraction as F

def om(p, eta=0.5):
    return p**eta / (p**eta + (1 - p)**eta) ** (1 / eta)

def om_closed(p):
    return math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))

print("L07 omega(3/10)=%.10f omega(3/5)=%.10f omega(1/2)=%.10f omega(1/4)=%.10f" % (om(.3), om(.6), om(.5), om(.25)))
print("closed-form check 1/4 vs 2-sqrt3 =", om_closed(.25), 2 - math.sqrt(3))
print("2*omega(3/10) = %.8f ; omega(3/5)=%.8f ; ratio = %.8f" % (2 * om(.3), om(.6), om(.3) / om(.6)))
print("ratio via closed form = %.8f" % (om_closed(.3) / om_closed(.6)))
print("threshold a=1: %.8f ; a=1/2: %.8f" % (1 / (1 + 2 ** -1), 1 / (1 + 2 ** -0.5)))
A = {0: F(2, 5), 50: F(3, 10), 100: F(3, 10)}
B = {0: F(2, 5), 100: F(3, 5)}
def gam(L, alpha, eta=0.5):
    return sum(om(float(p), eta) * float(x) ** alpha for x, p in L.items())
for al in (1.0, 0.5):
    print("alpha=%g Gamma(A)=%.8f Gamma(B)=%.8f diff=%.8f" % (al, gam(A, al), gam(B, al), gam(A, al) - gam(B, al)))
print("identity: V(A)=", sum(float(p) * x for x, p in A.items()), "V(B)=", sum(float(p) * x for x, p in B.items()))
print("omega(0.01)=%.8f omega(0.99)=%.8f" % (om(.01), om(.99)))
mis = om(.01) * 100 + om(.99) * 50
ev = .01 * 100 + .99 * 50
print("misc: weighted=%.6f ev=%.4f net=%.6f over=%.6f under=%.6f" % (mis, ev, mis - ev, (om(.01) - .01) * 100, (.99 - om(.99)) * 50))
print("printed-value check 8.3403+41.4925 = %.4f" % (8.3403 + 41.4925))
for p in (0.01, 0.05, 0.3, 0.5, 0.6, 0.95, 0.99):
    print("  p=%g omega=%.6f %s" % (p, om(p), "above" if om(p) > p else "below"))
grid = [i / 1000 for i in range(1001)]
ch = [om(p) > p for p in grid[1:-1]]
print("sign changes interior =", sum(1 for a, b in zip(ch, ch[1:]) if a != b))
above = [p for p in grid[1:-1] if om(p) > p]
print("last above grid point =", max(above), "om=%.8f vs %.3f ; next om=%.8f" % (om(max(above)), max(above), om(max(above) + .001)))
# crossing
lo, hi = 0.278, 0.279
for _ in range(100):
    mid = (lo + hi) / 2
    if om(mid) > mid: lo = mid
    else: hi = mid
print("crossing (bisection on omega-p) = %.8f" % lo)
gap = max(abs(om(p) - om_closed(p)) for p in grid)
print("closed-form largest gap eta=1/2: %.3e" % gap)
print("E2: unrounded diff =", gam(A, 1.0) - gam(B, 1.0))
# eta = 1 scenario
def om1(p): return p
print("ETA=1 closed form: largest gap between closed form and p over grid:", max(abs(om_closed(p) - p) for p in grid[1:-1]))
print("ETA=1 Gamma(A)=%.4f Gamma(B)=%.4f" % (sum(om1(float(p)) * x for x, p in A.items()), sum(om1(float(p)) * x for x, p in B.items())))
print("ETA=1 interior with omega>p count:", sum(1 for p in grid[1:-1] if om1(p) > p))
print("closed-form line with eta=1 would compare omega_1 vs closed:", max(abs(om1(p) - om_closed(p)) for p in grid))
print("R1 omega_1/2(1/2)=%.8f" % om(.5))
