"""Recompute the numeric claims of L05, L06 and L08 prose from first principles (not from the lab output)."""
import math
from fractions import Fraction

phi = (1 + math.sqrt(5)) / 2
print("L05 log_phi(501)", round(math.log(501) / math.log(phi), 4), "claimed 12.9186")
print("L05 log_phi(65)", round(math.log(65) / math.log(phi), 4), "claimed 8.6747")
print("L05 1/log2(phi)", round(1 / math.log2(phi), 6), "claimed 1.440420")
print("L05 ln3/lnphi", round(math.log(3) / math.log(phi), 2), "claimed 2.28")
print("L05 log_phi(377)", round(math.log(377) / math.log(phi), 2), "ln377", round(math.log(377), 3), "lnphi", round(math.log(phi), 4), "claimed 12.33, 5.932, 0.4812")
print("L05 log_phi(8)", round(math.log(8) / math.log(phi), 2), "claimed 4.32")
print("L05 272/500", 272 / 500, "63+53+2*(55+57)", 63 + 53 + 2 * (55 + 57))
print("L05 N(0..7)", end=" ")
N = [0, 1]
for h in range(2, 13):
    N.append(1 + N[h - 1] + N[h - 2])
print(N[:8], "N(12)", N[12])
print("L05 phi<2", phi < 2, "phi^2-phi-1", round(phi * phi - phi - 1, 12))
print("L05 log2 64 =", math.log2(64))
print("L06 40000/1438", round(40000 / 1438, 4), "E3 avg degree", 1238 / 200, "1438*27", 1438 * 27, 40000 - 1438 * 27, "/1438", round((40000 - 1438 * 27) / 1438, 4))
print("L06 572 =", 772 - 200, "sources sum n", 8 * (3 + 4 + 5 + 6 + 7), "pairs C(n,2) sum", 8 * sum(n * (n - 1) // 2 for n in range(3, 8)), "n^2 sum", 8 * sum(n * n for n in range(3, 8)))
print("L06 M1 check: none needed beyond the lab output")
print("L08 102/400", round(102 / 400, 4), "298+102", 298 + 102, "185-177", 185 - 177, "362=185+177", 185 + 177)
print("L08 floor(log2 7)+1", math.floor(math.log2(7)) + 1, "floor(log2 8)+1", math.floor(math.log2(8)) + 1)
print("L08 final bid < ask", 9980 < 9989)
print("L08 M1 share check: fills 2+3 =", 2 + 3)
print("L08 E1 102/398", round(102 / 398, 4))
