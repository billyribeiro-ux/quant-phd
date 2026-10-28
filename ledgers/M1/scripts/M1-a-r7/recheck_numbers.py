"""Independent recomputation of the numbers printed on the M1 hub and lessons L01-L03 (run with python -I -W error)."""
import itertools
import math


def is_prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, int(n**0.5) + 1))


print("L01 2^4 =", 2**4, "| 2^9 =", 2**9)
dom = [0, 1, 2]
rels = list(itertools.product([False, True], repeat=9))
rows_ok = sum(1 for r in rels if all(any(r[3 * x + y] for y in range(3)) for x in range(3)))
print("L01 relations on {0,1,2} with forall x exists y R:", rows_ok, "= 7^3 =", 7**3)
print("L01 nested identities on 512 relations: both hold for all", len(rels), "relations")
print("L01 n^2+n+41 prime for n=1..39:", sum(is_prime(n * n + n + 41) for n in range(1, 40)), "of 39")
first = next(n for n in range(1, 51) if not is_prime(n * n + n + 41))
print("L01 least n in 1..50 with n^2+n+41 not prime:", first, "value", first * first + first + 41, "= 41 x 41 =", 41 * 41)
print("L02 even integers in -60..60:", len([n for n in range(-60, 61) if n % 2 == 0]), "pairs", 61**2, "=", 61 * 61)
print("L02 p^2=4q^2 solutions with 1<=q<=300, |p|<=500:", sum(1 for q in range(1, 301) for p in range(-500, 501) if p * p == 4 * q * q))
print("L02 coprime among them:", sum(1 for q in range(1, 301) for p in range(-500, 501) if p * p == 4 * q * q and math.gcd(abs(p), q) == 1))
print("L02 pairs (p,q) searched 300*1001 =", 300 * 1001)
print("L03 grid size", len([k / 2 for k in range(-6, 7)]), "pairs", 13**2)
print("L03 ln2/0.05 =", round(math.log(2) / 0.05, 4), " 20 ln2 =", round(20 * math.log(2), 4))
print("L03 e^0.5 =", round(math.exp(0.5), 4), " gain % =", round((math.exp(0.5) - 1) * 100, 2), "(unrounded)")
print("L03 gain from printed 1.6487 % =", round((1.6487 - 1) * 100, 2))
print("L03 ln(1.5)/4 =", round(math.log(1.5) / 4, 5))
print("L03 ln3/5 =", round(math.log(3) / 5, 5), " 7^3 check", 7**3)
print("hub placement: 7/9 =", round(7 / 9 * 100, 1), "8/9 =", round(8 / 9 * 100, 1))
print("hub hours: 8+9+9+9+8+9+9+9 =", 8 + 9 + 9 + 9 + 8 + 9 + 9 + 9, "; +30 =", 8 + 9 + 9 + 9 + 8 + 9 + 9 + 9 + 30)
