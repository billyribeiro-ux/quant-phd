"""Round 10 closed-form checks for cards c053, c115, c124, c140, c149, c150, c159, c174, c183, c187, c201, c205 (stdlib only)."""
import math
from math import erfc, exp, pi, sqrt

print("c115 erfc(1/sqrt2) =", round(erfc(1 / sqrt(2)), 10))
print("c174 P(tau_1<=1)=2(1-Phi(1)) =", round(erfc(1 / sqrt(2)), 6), " P(tau_1<=2)=erfc(1/2) =", round(erfc(0.5), 6))
f = lambda a, H: a * H ** -1.5 * exp(-a * a / (2 * H)) / sqrt(2 * pi)
print("c174 f_1(1) =", round(f(1, 1), 6), " f_1(2) =", round(f(1, 2), 6))
print("c201 1-Phi(1) =", round(0.5 * erfc(1 / sqrt(2)), 10))
print("c053 H*sqrt(2/N)/20 at H=2,N=1 =", round(2 * sqrt(2) / 20, 5), " at H=2,N=128 =", round(2 * sqrt(2 / 128) / 20, 6))
print("c187 rel gap H=2,N=1 =", round(100 * (0.1601 / (2 * sqrt(2) / 20) - 1), 2), "%; H=2,N=2 =", round(100 * (0.0934 / (2 * sqrt(2 / 2) / 20) - 1), 2), "%")
print("c159 SE k=121 n=400 =", round(sqrt(121 * 279 / (400 ** 2 * 399)), 4))
print("c149 SE 4 steps =", round(sqrt(0.2275 * 0.7725 / 400), 4), " SE 256 steps =", round(sqrt(0.3025 * 0.6975 / 400), 4))
print("c150 gap in SE =", round((sqrt(2 / pi) - 0.7586) / 0.0317, 3), " (sqrt(2/pi)=", round(sqrt(2 / pi), 6), ")")
print("c183 log-derivative zero at H=a^2/3: (a^2-3H)/(2H^2) at a=1, H=1/3 =", (1 - 3 * (1 / 3)) / (2 * (1 / 3) ** 2))
print("c205/c201 2(1-Phi(1)) =", round(2 * 0.5 * erfc(1 / sqrt(2)), 6))
print("c140 2*sqrt(H)/sqrt(2pi) at H=1 =", round(2 / sqrt(2 * pi), 6), " sqrt(2/pi) =", round(sqrt(2 / pi), 6))
print("c170 sum n2^n n=1..12 =", sum(n * 2 ** n for n in range(1, 13)))
print("c174 central check H=1 density (a=1) =", round(f(1, 1), 6))
