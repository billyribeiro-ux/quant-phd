"""Independent Chapman-Kolmogorov check for L05 (round 11): trapezoid rule with a different grid from the twin.

Standard library only. Run: python -I -W error ck_independent_r11.py
"""
import math

def p(u, x, y):
    return math.exp(-((y - x) ** 2) / (2 * u)) / math.sqrt(2 * math.pi * u)

def trap(f, a, b, n):
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h

cases = 0
worst = 0.0
worst_tail = 0.0
for s in (0.5, 1.0, 2.0):
    for t in (0.5, 1.0, 2.0):
        for x in (-1.0, -0.25, 0.0, 0.5, 1.0):
            for y in (-1.0, -0.25, 0.0, 0.5, 1.0):
                cases += 1
                integral = trap(lambda z: p(s, x, z) * p(t, z, y), -14.0, 14.0, 6000)
                worst = max(worst, abs(integral - p(s + t, x, y)))
                tail = trap(lambda z: p(s, x, z) * p(t, z, y), 12.0, 40.0, 4000) + \
                    trap(lambda z: p(s, x, z) * p(t, z, y), -40.0, -12.0, 4000)
                worst_tail = max(worst_tail, tail)
print("independent CK cases", cases, "largest |trapezoid gap| %.3e" % worst, "below 1e-6:", worst < 1e-6)
print("largest tail mass 12<=|z|<=40 (trapezoid) %.3e" % worst_tail)
for t in (0.5, 1.0, 2.0):
    print("trapezoid integral of p_%g(0,y) over [-12,12] = %.10f" % (t, trap(lambda y: p(t, 0.0, y), -12.0, 12.0, 6000)))
