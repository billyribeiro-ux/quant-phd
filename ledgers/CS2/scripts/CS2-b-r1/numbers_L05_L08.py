"""Independent recomputation of the prose numbers in CS2 L05-L08 (verifier round 1, slice CS2-b).

Run: <checkout>/.venv/bin/python -I <checkout>/ledgers/CS2/scripts/CS2-b-r1/numbers_L05_L08.py
Every value is recomputed here with code written separately from the lab twins.
"""
import math
from fractions import Fraction

PHI = (1 + math.sqrt(5)) / 2

print("L05 arithmetic")
print("N(0..7) recurrence:", end=" ")
N = [0, 1]
for h in range(2, 13):
    N.append(1 + N[h - 1] + N[h - 2])
print(N[:8])
print("N(5) =", N[5], " N(12) =", N[12], " N(4)=", N[4])
print("log_phi(501) =", round(math.log(501) / math.log(PHI), 4))
print("log_phi(65) =", round(math.log(65) / math.log(PHI), 4))
print("1/log2(phi) =", round(1 / math.log2(PHI), 6))
print("ln 377 =", round(math.log(377), 4), " ln phi =", round(math.log(PHI), 4), " log_phi 377 =", round(math.log(377) / math.log(PHI), 4))
print("log_phi 3 =", round(math.log(3) / math.log(PHI), 4), " log_phi 8 =", round(math.log(8) / math.log(PHI), 4))
print("272/500 =", Fraction(272, 500), "=", 272 / 500 * 100, "%")
print("63+53+2*(55+57) =", 63 + 53 + 2 * (55 + 57))
print("phi^2 - (phi+1) =", PHI * PHI - (PHI + 1))
print("phi < 2:", PHI < 2)
print("N(h)+1 >= phi^h for h=1..12:", all(N[h] + 1 >= PHI ** h for h in range(1, 13)))
print("N(h)+1 vs phi^h printed at h=12:", N[12] + 1, round(PHI ** 12, 4))
print("log2(64) =", math.log2(64), " 2^40 =", 2 ** 40, " bits(2^40) =", (2 ** 40).bit_length())
print("2^20+1 =", 2 ** 20 + 1, " bits(2^20) =", (2 ** 20).bit_length())
print("bits(1000) =", (1000).bit_length())

print("\nL06 arithmetic")
print("40000/1438 =", round(40000 / 1438, 4), " 1438*27 =", 1438 * 27, " remainder", 40000 - 1438 * 27)
print("772-200 =", 772 - 200, " 1238/200 =", 1238 / 200, " 2*619 =", 2 * 619)
print("sum n^2 over 40 graphs:", sum((3 + k % 5) ** 2 for k in range(40)), " pairs n(n-1)/2:", sum((3 + k % 5) * (2 + k % 5) // 2 for k in range(40)))
print("n(n-1) for n=200 complete check: 200*199 =", 200 * 199)
print("triangle degree sum", 2 + 2 + 2)

print("\nL07 arithmetic")
print("LCS table cells m+1 by n+1 for 5x8:", 6 * 9, " mn:", 5 * 8, " boundary:", 6 * 9 - 5 * 8)
print("coin table entries A=1024:", 1024 + 1)
print("1/log2 phi check via ln:", round(math.log(2) / math.log(PHI), 6))

print("\nL08 arithmetic")
print("102/400 =", 102 / 400, " 298+102 =", 298 + 102, " 185-177 =", 185 - 177, " 185+177 =", 185 + 177)
print("9980 < 9989:", 9980 < 9989, " 7 bits:", (7).bit_length(), " 8 bits:", (8).bit_length())
print("bit_length 8..15 == 4:", all((L).bit_length() == 4 for L in range(8, 16)), " 7 is 4?", (7).bit_length() == 4)
