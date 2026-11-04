"""Independent exact recomputation of the SC1 L06 numbers quoted on cards and the page (stdlib only, read-only).

Enumerates walks directly (no reuse of the lab code) and prints exact fractions and the erfc values.
"""
import math
from fractions import Fraction
from itertools import product


def walks(n):
    for steps in product((1, -1), repeat=n):
        s, m, path = 0, 0, []
        for e in steps:
            s += e
            m = max(m, s)
        yield m, s


# Card c113: N = 10, a = 2
w10 = list(walks(10))
p_max = Fraction(sum(1 for m, s in w10 if m >= 2), 1024)
p_above = Fraction(sum(1 for m, s in w10 if s > 2), 1024)
p_eq = Fraction(sum(1 for m, s in w10 if s == 2), 1024)
print("N=10 a=2: P(M>=2)=", p_max, " 2P(S>2)=", 2 * p_above, " P(S=2)=", p_eq,
      " diff=", p_max - 2 * p_above, " diff==P(S=2):", p_max - 2 * p_above == p_eq)
# Card c114: N = 12, a = 3, S_12 = 2 and S_12 = 4
w12 = list(walks(12))
print("N=12 a=3: #{M>=3, S=2}=", sum(1 for m, s in w12 if m >= 3 and s == 2),
      " #{S=4}=", sum(1 for m, s in w12 if s == 4), " total=", len(w12))
# Card c111 / c112: counts over all N <= 12
triples = equal = 0
pairs = pairs_eq = 0
for n in range(1, 13):
    ws = list(walks(n))
    for a in range(1, n + 1):
        pairs += 1
        pairs_eq += sum(1 for m, s in ws if m >= a) == sum(1 for m, s in ws if s >= a) + sum(1 for m, s in ws if s > a)
        for b in range(-n, a):
            triples += 1
            equal += sum(1 for m, s in ws if m >= a and s == b) == sum(1 for m, s in ws if s == 2 * a - b)
print("triples", triples, "equal", equal, "pairs", pairs, "tail equal", pairs_eq)
# Card c115 / c124 / E3: erfc values
print("erfc(1/sqrt2) =", f"{math.erfc(1 / math.sqrt(2)):.12f}", " half =", f"{math.erfc(1 / math.sqrt(2)) / 2:.12f}")
# Card c124 check: 2P(B_t>a) = erfc(a/sqrt(2t)) at t=1,a=1 via normal tail
tail = 0.5 * math.erfc(1 / math.sqrt(2))
print("P(B_1>1) =", f"{tail:.12f}")
