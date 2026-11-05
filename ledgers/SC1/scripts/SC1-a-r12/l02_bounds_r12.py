"""Independent recomputation of the L02 Lab 1 bound lines and the tail-bound sum, from the seed, without the twin's code path.
Usage: python -I l02_bounds_r12.py"""
import math
import random

rng = random.Random(20260101)
xi0 = rng.gauss(0.0, 1.0)
coeffs = {m: [rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, 9)}
bound = {m: math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2) for m in range(1, 9)}
obs = {m: max(abs(c) for c in coeffs[m]) * 2 ** (-(m + 1) / 2) for m in range(1, 9)}
for m in range(1, 9):
    print(f"m = {m}: observed sup {obs[m]:.6f}, bound {bound[m]:.6f}, observed <= bound: {obs[m] <= bound[m]}")
print(f"sum of bounds for levels 5 to 8: {sum(bound[m] for m in range(5, 9)):.6f}")
print(f"sqrt(4 log 2)/2 = {math.sqrt(4*math.log(2))/2:.7f}; 2^-1 bound check m=1 -> {bound[1]:.7f}")
print("M_m closed form check, m=1..8 (max abs diff):",
      max(abs(bound[m] - math.sqrt(2*math.log(2))*math.sqrt(m)*2**(-m/2)) for m in range(1, 9)))
