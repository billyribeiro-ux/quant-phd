"""Round 5 verifier: find a zero-coupon bond whose exact price has fractional part just under one half."""
from fractions import Fraction
n, b = 3, 1
D = (10_000 + b) ** n
# price = f * 10000**n / D ; want f*10000**n == (D-1)/2 (mod D)
target = (D - 1) // 2
f = target * pow(pow(10_000, n, D), -1, D) % D
if f == 0:
    f = D
price = Fraction(f * 10_000**n, D)
frac = price - (price.numerator // price.denominator)
print("n", n, "b", b, "D", D, "face", f)
print("exact price", float(price), "fraction", frac, "frac - 1/2", frac - Fraction(1, 2))
print("nearest cent (exact, half away)", (2 * price.numerator + price.denominator) // (2 * price.denominator))
print("floor", price.numerator // price.denominator)
