"""Independent recomputation of the printed and prose numbers of L08-L10 (round 4, verifier M4-c)."""
import math
from fractions import Fraction
from statistics import NormalDist
from scipy import integrate

phi1 = NormalDist().cdf(1)
fV = lambda t: 2 / (math.pi * math.sqrt(3)) * (1 + t * t / 3) ** -2
fC = lambda x: 1 / (math.pi * (1 + x * x))
print("L10 P(|C|>10) quad:", 2 * integrate.quad(fC, 10, math.inf)[0], "closed:", 2 / math.pi * math.atan(0.1))
print("L10 P(|V|>10) quad:", 2 * integrate.quad(fV, 10, math.inf)[0])
print("L10 F_V(2)-F_V(-2) quad:", integrate.quad(fV, -2, 2)[0])
print("L10 10*P(|C|>10):", 10 * 2 / math.pi * math.atan(0.1), "gap to 2/pi:", 2 / math.pi - 10 * 2 / math.pi * math.atan(0.1))
print("L10 1/0.063451 =", 1 / 0.063451, "0.4116/0.1279 =", 0.4116 / 0.1279, "1.8220/sqrt10 =", 1.8220 / math.sqrt(10))
print("L10 F_V(sqrt3) =", 0.75 + 1 / (2 * math.pi), " 4sqrt3/pi =", 4 * math.sqrt(3) / math.pi)
for n in (1, 5, 10, 20, 40):  # L09 Part A, exact, offsets = face - 1
    poly = [1]
    for _ in range(n):
        new = [0] * (len(poly) + 5)
        for i, c in enumerate(poly):
            for f in range(6):
                new[i + f] += c
        poly = new
    thr = math.floor(3.5 * n + math.sqrt(35 * n / 12))
    p = Fraction(sum(poly[: thr - n + 1]), 6**n)
    print(f"L09 A n={n} thr={thr} P={float(p):.6f} gap={float(p) - phi1:+.6f}")
print("L09 E1 threshold:", 35 + math.sqrt(35 * 10 / 12))
print("L09 E2 gap (0.8552):", 0.8552 - phi1, "SE:", math.sqrt(0.8552 * 0.1448 / 4000), "gap/SE:", (0.8552 - phi1) / math.sqrt(0.8552 * 0.1448 / 4000))
print("L09 M1 7/60 =", 7 / 60, "M2 35/48 =", 35 / 48, "E3 bound =", (35 / 12) / (10000 * 0.25))
