"""Round-5 re-derivation of the numbers in the M5 L08-L10 delta (independent of the page text)."""
import math
from fractions import Fraction

D = math.sqrt(3) / 2
TAU = 1e-12
print("E1 a priori thresholds (tau=1e-12, Delta=sqrt(3)/2):")
for b in (0.5, 0.9, 0.95):
    t = math.log(TAU * (1 - b) / D) / math.log(b)
    n = math.ceil(t)
    print(f"  beta={b} threshold={t:.2f} least_n={n} holds_at_n={b**n * D / (1 - b) <= TAU} fails_at_n-1={b**(n-1) * D / (1 - b) <= TAU}")
print("L09 R2 a priori bound (beta=0.9, ||V1-V0||=sqrt(3)/2):")
for n in (147, 151, 152):
    print(f"  n={n} bound={0.9**n * D / 0.1:.6e}")
n = 1
while 0.9**n * D / 0.1 > 1e-6:
    n += 1
print(f"  smallest n with bound <= 1e-6: {n}; 0.9^n threshold {1e-6 * 0.1 / D:.6e}")
print("L08 Example 1.2 / M3 / E2 / quiz values:")
print(f"  sqrt(0.75)={math.sqrt(0.75):.6f} sqrt(0.5)={math.sqrt(0.5):.6f} sqrt(0.5)-0.25={math.sqrt(0.5)-0.25:.6f}")
print(f"  utility={math.sqrt(math.sqrt(0.5)-0.25):.6f} V*(0.5)={0.9*5+math.sqrt(math.sqrt(0.5)-0.25):.6f}")
print("L10 Example 3.3 closed forms (exact):")
for n in (4, 10, 100, 1000):
    r = Fraction((n + 1) * (4 * n - 1), 6 * n * n)
    l = Fraction(4 * n * n - 3 * n - 1, 6 * n * n)
    rd = r - Fraction(2, 3)
    ld = l - Fraction(2, 3)
    print(f"  n={n} right={float(r):.12f} left={float(l):.12f} right-2/3={rd} <=1/(2n):{rd <= Fraction(1, 2 * n)} "
          f"left-2/3={ld} |.|<=2/(3n):{abs(ld) <= Fraction(2, 3 * n)} <=1/n:{abs(ld) <= Fraction(1, n)}")
    # direct sums from the tagged definition
    right = sum(Fraction(i, n) * (Fraction(i, n) ** 2 - Fraction(i - 1, n) ** 2) for i in range(1, n + 1))
    left = sum(Fraction(i - 1, n) * (Fraction(i, n) ** 2 - Fraction(i - 1, n) ** 2) for i in range(1, n + 1))
    print(f"    direct_sums_match={right == r and left == l}")
