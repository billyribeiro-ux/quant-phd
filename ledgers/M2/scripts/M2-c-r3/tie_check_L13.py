"""L13 Misconception/Key result tie claim: central error at h=1e-5 vs h=1e-7 differ by < 1e-15 (verifier round 3)."""
import math
e = math.e
def cen(h): return abs((math.exp(1 + h) - math.exp(1 - h)) / (2 * h) - e)
print("central 1e-5", cen(1e-5), "central 1e-7", cen(1e-7), "difference", abs(cen(1e-5) - cen(1e-7)), "less than 1e-15:", abs(cen(1e-5) - cen(1e-7)) < 1e-15)
