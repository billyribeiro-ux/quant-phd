"""SC1-b round 7: independent check of the L05 tail-mass and window-mass claims (different quadrature, math.fsum)."""
import math

def p(u, x, y):
    return math.exp(-((y - x) ** 2) / (2 * u)) / math.sqrt(2 * math.pi * u)

def simp(f, a, b, n):
    h = (b - a) / n
    vals = [f(a + i * h) for i in range(n + 1)]
    s = vals[0] + vals[-1] + 4 * math.fsum(vals[1:-1:2]) + 2 * math.fsum(vals[2:-1:2])
    return s * h / 3

TIMES = (0.5, 1.0, 2.0)
POINTS = (-1.0, -0.25, 0.0, 0.5, 1.0)
worst_tail = 0.0
worst_gap = 0.0
for s in TIMES:
    for t in TIMES:
        for x in POINTS:
            for y in POINTS:
                f = lambda z: p(s, x, z) * p(t, z, y)
                tail = simp(f, 12, 40, 4000) + simp(f, -40, -12, 4000)
                worst_tail = max(worst_tail, tail)
                gap = simp(f, -12, 12, 4000) - p(s + t, x, y)
                worst_gap = max(worst_gap, abs(gap))
print(f"independent: largest tail mass 12<=|z|<=40: {worst_tail:.3e} (lab prints 3.81e-29 for 2000 intervals)")
print(f"independent: largest |gap| with n=4000 Simpson, [-12,12]: {worst_gap:.3e} (lab prints 5.55e-16 with n=2000)")
print("window mass check:", [f"{simp(lambda y: p(t,0.0,y), -12, 12, 4000):.12f}" for t in TIMES])
