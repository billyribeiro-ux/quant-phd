"""L13 sweep minima over h = 10^-k, k = 1..12, unrounded (verifier round 3). Standard library only."""
import math
e = math.e
def fwd(h): return abs((math.exp(1 + h) - math.exp(1)) / h - e)
def cen(h): return abs((math.exp(1 + h) - math.exp(1 - h)) / (2 * h) - e)
print("forward min over decades:", min((fwd(10.0 ** -k), k) for k in range(1, 13)))
print("central min over decades:", min((cen(10.0 ** -k), k) for k in range(1, 13)))
print("forward at 1e-8:", fwd(1e-8))
