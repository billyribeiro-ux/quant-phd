"""Independent recomputation of CS2 L11 bounds and capacities (verifier round 4)."""
import math
from fractions import Fraction


def cap(h, eps):
    return 2 * math.ceil(Fraction((h + 1) * (h + 2), 2) / eps)


def closed(L, eps):
    return Fraction((L + 1) * (L + 2) * (L + 3), 3) / eps + (L + 1)


e20 = Fraction(1, 20)
e10 = Fraction(1, 10)
print("closed form L=29 eps=1/20:", closed(29, e20), "| floor(log2 1e9) =", math.floor(math.log2(10**9)))
print("closed form L=12 eps=1/20:", closed(12, e20), "| exact Cor 2.6 sum L=12:", sum(cap(h, e20) - 1 for h in range(13)))
print("exact Cor 2.6 sum L=29 eps=1/20:", sum(cap(h, e20) - 1 for h in range(30)))
print("capacities eps=1/20:", [cap(h, e20) for h in range(5)], "eps=1/10:", [cap(h, e10) for h in range(3)])
print("Thm 2.2(b) level bounds eps=1/20 n=5000:", [5000 // (cap(h, e20) * 2**h) for h in range(5)], "sum", sum(5000 // (cap(h, e20) * 2**h) for h in range(5)))
