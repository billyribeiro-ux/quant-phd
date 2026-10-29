# Independent recomputation of the numbers that the changed or re-read rows cite (round 23).
import math

def npv(flows, rate):
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(flows))

# L03 real and nominal project
real = (-100_000_000, 30_000_000, 30_000_000, 30_000_000, 30_000_000, 30_000_000)
r, pi = 0.06, 0.03
n = (1 + r) * (1 + pi) - 1
nom = [cf * (1 + pi) ** t for t, cf in enumerate(real)]
real_npv = npv(real, r)
print("n", round(n, 10), "additive gap", round(n - (r + pi), 10), "r*pi", r * pi)
print("real NPV USD", round(real_npv / 100, 2), "consistent", round(npv(nom, n) / 100, 2))
mixed_over = npv(nom, r)
mixed_under = npv(real, n)
print("mixed over USD", round(mixed_over / 100, 2), "mixed under USD", round(mixed_under / 100, 2))
gap = (mixed_over - real_npv) / 100
print("mixed gap USD", round(gap, 2))
print("gap share at 0.03 (113637.49/263709.14)", round(113637.49 / 263709.14, 4), round(113637.49 / 263709.14 * 100, 1))
print("share at 0.05 (194368.27/263709.14)", round(194368.27 / 263709.14, 5), round(194368.27 / 263709.14 * 100, 1))
print("share at 0.01 (36913.22/263709.14)", round(36913.22 / 263709.14 * 100, 2))
print("(1+r)(1+pi)-1 r=.10 pi=.10:", round(1.10 * 1.10 - 1, 4))
print("Example 2.5 nominal NPV:", round(100 / 1.08 + 100 / 1.08**2 + 100 / 1.08**3, 4), "real rate", round(1.08 / 1.03 - 1, 6))
print("M2 nominal", round(1000 * 1.02**3, 3))
print("M3 real rate", round(1.10 / 1.04 - 1, 6), "PV", round(104 / 1.10, 3))
print("P3 sqrt(0.005)", round(math.sqrt(0.005), 6))
print("R2 ratio", round(0.06 * 1.03 / 0.03, 4))
print("R3 b", round(1.06 / 2.03, 6))
print("E3 nominal", round(1.10 * 1.03 - 1, 6))
print("two-line example", round(200 / 1.05, 3), round(205 * 1.05 / 200 - 1, 5), round(1.07625 / 1.05 - 1, 6))
# L04
P = (-10_000_000, 23_000_000, -13_200_000)
print("P NPV 15%", round(npv(P, 0.15) / 100, 2), "5%", round(npv(P, 0.05) / 100, 2))
print("closed form 5%", round(-2000 * (11 / 1.05 - 10) * (6 / 1.05 - 5), 2))
print("avg of IRRs NPV at 15%", round(npv(P, 0.15) / 100, 2))
A = (-10_000_000, 13_000_000)
B = (-20_000_000, 25_000_000)
print("Ex4.2 NPV A", round(npv(A, 0.10) / 100, 2), "B", round(npv(B, 0.10) / 100, 2), "at 20", round(npv(A, .2) / 100, 2), round(npv(B, .2) / 100, 2))
print("E2 变体 A(-100k,120k) at 10/35:", round(npv((-100000, 120000), 0.10), 2), round(npv((-100000, 120000), 0.35), 2), "B", round(npv((-200000, 250000), 0.10), 2), round(npv((-200000, 250000), 0.35), 2))
print("E2 crossover", 130000 / 100000 - 1)
print("M2 L04 x root", (-1 + math.sqrt(23 / 3)) / 2, "r", 1 / ((-1 + math.sqrt(23 / 3)) / 2) - 1)
print("R1 NPV at 10%", round(-1 + 6 / 1.1 - 5 / 1.21, 6))
print("R2 sqrt3-1", round(math.sqrt(3) - 1, 6), "NPV_A 10%", round(300 / 1.21 - 100, 2), "NPV_B", round(200 / 1.1 - 100, 2))
print("R3 FV 15%", round(1.15**2 * npv(P, 0.15), 2), "FV 5%", round(1.05**2 * npv(P, 0.05), 2))
print("Remark 5.1 FV at 20%", -100000 * 1.2**2 + 230000 * 1.2 - 132000)
print("M1 IRR", 121 / 100 - 1)
# verify factorization against direct NPV at a few rates
for rr in (-0.4, 0.0, 0.05, 0.15, 0.5, 2.0):
    x = 1 / (1 + rr)
    assert abs(npv(P, rr) - (-200000 * (11 * x - 10) * (6 * x - 5))) < 1e-6, rr
print("factorization agrees at six test rates")
