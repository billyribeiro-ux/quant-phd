"""Independent recomputation of L07 numbers (E3-c round 2). Uses fractions/decimal-free floats at full precision."""
import math
from fractions import Fraction

def om(p, eta=0.5):
    return p**eta / (p**eta + (1 - p)**eta) ** (1 / eta)

def om_closed(p):
    return math.sqrt(p) / (1 + 2 * math.sqrt(p * (1 - p)))

print("omega(0.3)", repr(om(0.3)), om_closed(0.3))
print("omega(0.6)", repr(om(0.6)), om_closed(0.6))
print("omega(0.5)", repr(om(0.5)), 1 / (2 * math.sqrt(2)))
print("omega(0.01)", repr(om(0.01)), "omega(0.05)", om(0.05), "omega(0.99)", repr(om(0.99)), "omega(0.95)", om(0.95))
print("omega(0.25)", om(0.25), "2-sqrt3", 2 - math.sqrt(3))
print("2*omega(0.3)", 2 * om(0.3))
r = om(0.3) / om(0.6)
print("ratio unrounded", repr(r))
print("ratio of printed 8dp", 0.28579088 / 0.39125077)
print("threshold a=1", 1 / (1 + 2 ** -1), "a=0.5", 1 / (1 + 2 ** -0.5))
VA1 = om(0.3) * (50 + 100); VB1 = om(0.6) * 100
print("V(A) a=1", repr(VA1), "V(B) a=1", repr(VB1), "diff", repr(VA1 - VB1))
VA2 = om(0.3) * (50 ** 0.5 + 100 ** 0.5); VB2 = om(0.6) * 100 ** 0.5
print("V(A) a=.5", repr(VA2), "V(B) a=.5", repr(VB2))
print("printed diff 42.8686-39.1251", 42.8686 - 39.1251)
# Misconception 3
w1 = om(0.01); w99 = om(0.99)
v = w1 * 100 + w99 * 50
print("L value", v, "w1*100", w1 * 100, "w99*50", w99 * 50, "EV", 0.01 * 100 + 0.99 * 50)
print("overweight", (w1 - 0.01) * 100, "underweight", (0.99 - w99) * 50, "net", v - 50.5)
print("with rounded 0.0834 and 0.8298:", (0.0834 - 0.01) * 100, (0.99 - 0.8298) * 50)
# M2
print("M2", om(0.5) * 100)
# Crossing
lo, hi = 0.278, 0.279
for _ in range(200):
    mid = (lo + hi) / 2
    if om(mid) > mid:
        lo = mid
    else:
        hi = mid
print("crossing", lo, hi)
# sign-change check on grid
grid = [i / 1000 for i in range(1001)]
ab = [om(p) > p for p in grid[1:-1]]
print("changes", sum(1 for a, b in zip(ab, ab[1:]) if a != b), "last above", max(p for p in grid[1:-1] if om(p) > p))
print("first interior above?", ab[0])
print("max closed gap", max(abs(om(p) - om_closed(p)) for p in grid[1:-1]))
# Remark 2.3 identity
print("identity V(A) a=1", 0.3 * 50 + 0.3 * 100, "V(B)", 0.6 * 100)
# Prop 2.2 iff check at a=1 and a=0.5
for a in (1.0, 0.5):
    VA = om(0.3) * (50 ** a + 100 ** a); VB = om(0.6) * 100 ** a
    print("alpha", a, VA > VB)
# Alternative: check lab's expected ETA-setting prediction
print("eta=1 om(0.3)", om(0.3, 1.0), "V", om(0.3,1.0)*150, om(0.6,1.0)*100)
# ETA-set check of 'omega(p)=p' with eta=1: p**1/(p+(1-p))**1
