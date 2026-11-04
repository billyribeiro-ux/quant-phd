"""Re-derive the L02 Lab 1 printed numbers and the E3 digits from the seed, independently of the lab file.
Usage: python -I l02_numbers.py"""
import math
import random

rng = random.Random(20260101)
xi0 = rng.gauss(0.0, 1.0)
coeffs = [[rng.gauss(0.0, 1.0) for _ in range(2 ** (m - 1))] for m in range(1, 9)]
for m in range(1, 9):
    sup = max(abs(c) for c in coeffs[m - 1]) * 2 ** (-(m + 1) / 2)
    bnd = math.sqrt(4 * m * math.log(2)) * 2 ** (-(m + 1) / 2)
    print(f"m={m} sup={sup:.9f} printed={sup:.6f} bound={bnd:.9f} printed={bnd:.6f} within={sup <= bnd}")
x11 = abs(coeffs[0][0])
print("abs xi_{1,1} =", repr(x11), "rounded 6dp:", f"{x11:.6f}")
print("2 * printed sup 0.116589 =", 2 * 0.116589)
print("2 * unrounded sup =", 2 * max(abs(c) for c in coeffs[0]) * 2 ** -1)
print("sqrt(4 log 2) =", math.sqrt(4 * math.log(2)), "half =", math.sqrt(4 * math.log(2)) / 2)
# tail check of the lab's last line on the 1/2^10 grid
def hat(m, j, t):
    centre = (2 * j - 1) / 2.0**m
    return max(0.0, 1.0 - 2.0**m * abs(t - centre))
def psum(levels, t):
    total = xi0 * t
    for m in range(1, levels + 1):
        for j in range(1, 2 ** (m - 1) + 1):
            total += coeffs[m - 1][j - 1] * 2 ** (-(m + 1) / 2) * hat(m, j, t)
    return total
grid = [i / 2**10 for i in range(2**10 + 1)]
print("grid sup |S8-S4| =", f"{max(abs(psum(8, t) - psum(4, t)) for t in grid):.6f}")
print("sum bounds 5..8 =", f"{sum(math.sqrt(4*m*math.log(2))*2**(-(m+1)/2) for m in range(5,9)):.6f}")
