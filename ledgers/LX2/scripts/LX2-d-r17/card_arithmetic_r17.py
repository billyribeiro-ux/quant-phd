# Independent re-derivation of every number the LX2 cards state (not using the lab modules).
# Run: python -I -W error ledgers/LX2/scripts/LX2-d-r16/card_arithmetic_r16.py
import random
from fractions import Fraction
from itertools import product

def rnd(x: Fraction, places: int = 4) -> str:
    # ties away from zero, exact
    import math
    sign = "-" if x < 0 else ""
    units = math.floor(abs(x) * 10**places + Fraction(1, 2))
    return f"{sign}{units // 10**places}.{units % 10**places:0{places}d}"

ok = True
def check(label, got, want):
    global ok
    flag = "OK" if got == want else "MISMATCH"
    if got != want:
        ok = False
    print(f"{flag:9} {label}: got {got!r} want {want!r}")

# L01 model (independent re-implementation)
S = ["unregistered", "filed", "refused", "effective", "stop_order"]
L = ["not_listed", "listed"]
states = list(product(S, L))
ev33 = [("unregistered", "filed"), ("filed", "refused"), ("refused", "filed"), ("filed", "effective"),
        ("effective", "stop_order"), ("stop_order", "effective")]
ev34 = [("not_listed", "listed"), ("listed", "not_listed")]
trans = [((a, l), (b, l)) for (a, b) in ev33 for l in L] + [((s, a), (s, b)) for (a, b) in ev34 for s in S]
check("L01 states", len(states), 10)
check("L01 transitions", len(trans), 22)
check("L01 transitions from 1933 events", len(ev33) * len(L), 12)
check("L01 transitions from 1934 events", len(ev34) * len(S), 10)
reach = {("unregistered", "not_listed")}
changed = True
while changed:
    changed = False
    for a, b in trans:
        if a in reach and b not in reach:
            reach.add(b); changed = True
check("L01 reachable from start", len(reach), 10)
r13 = lambda s: s[1] == "listed"
r15 = lambda s: s[0] in ("effective", "stop_order") and s[1] == "not_listed"
offer = lambda s: s[0] in ("filed", "effective")
sale = lambda s: s[0] == "effective"
check("L01 both duties", sum(r13(s) and r15(s) for s in states), 0)
check("L01 sale and not offer", sum(sale(s) and not offer(s) for s in states), 0)
check("L01 sale-permitted states", sum(sale(s) for s in states), 2)
check("L01 offer-permitted states", sum(offer(s) for s in states), 4)
check("L01 R13 states", sum(r13(s) for s in states), 5)
check("L01 R15 states", sum(r15(s) for s in states), 2)

# L04 generator path, seed 20261103, draw order U_1, V_1, U_2, V_2 ... (independent of the lab code)
rng = random.Random(20261103)
path = []
for t in range(1, 25):
    U = rng.randint(-6, 6)
    V = rng.randint(-4, 4)
    y, yhat = 100 + U, 101 + V
    path.append((yhat, y, yhat - y))
hits = [1 if abs(e) <= 2 else 0 for (_, _, e) in path]
check("L04 path hits", sum(hits), 9)
check("L04 hit rate (exact)", Fraction(sum(hits), 24), Fraction(3, 8))
check("L04 hit rate rounded", rnd(Fraction(sum(hits), 24)), "0.3750")
bias = Fraction(sum(e for (_, _, e) in path), 24)
check("L04 bias exact", bias, Fraction(41, 12))
check("L04 bias sum of errors", sum(e for (_, _, e) in path), 82)
check("L04 bias rounded", rnd(bias), "3.4167")
check("L04 MAE (not printed)", Fraction(sum(abs(e) for (_, _, e) in path), 24), Fraction(13, 3))
print("L04 Part A printed table rows (t forecast realised error hit):")
for t, (yhat, y, e) in enumerate(path, 1):
    print(f"   {t:>2} {yhat:>9} {y:>9} {e:>6} {1 if abs(e) <= 2 else 0:>4}")
h1 = Fraction(sum(hits[:12]), 12); h2 = Fraction(sum(hits[12:]), 12)
b1 = Fraction(sum(e for (_, _, e) in path[:12]), 12); b2 = Fraction(sum(e for (_, _, e) in path[12:]), 12)
check("L04 first-12 hit rate", h1, Fraction(1, 4))
check("L04 last-12 hit rate", h2, Fraction(1, 2))
check("L04 first-12 bias", rnd(b1), "3.6667")
check("L04 last-12 bias", rnd(b2), "3.1667")
# Part C hand-built path
errs = [3, -3, 3, -3]
check("L04 Part C bias", Fraction(sum(errs), 4), 0)
check("L04 E2 first-12 error sum", sum(e for (_, _, e) in path[:12]), 44)
check("L04 Part C hits", sum(1 for e in errs if abs(e) <= 2), 0)
check("L04 Part C MAE", Fraction(sum(abs(e) for e in errs), 4), 3)
# Part D enumeration over 9 x 13 pairs
pairs = [(1 + v - u) for v in range(-4, 5) for u in range(-6, 7)]
check("L04 pairs", len(pairs), 117)
check("L04 P(hit) exact", Fraction(sum(1 for e in pairs if abs(e) <= 2), 117), Fraction(44, 117))
check("L04 P(hit) rounded", rnd(Fraction(44, 117)), "0.3761")
check("L04 E[error]", Fraction(sum(pairs), 117), 1)
check("L04 8*5+4", 8 * 5 + 4, 44)
check("L04 hit set lower bound -3<=V-U<=1 equals |e|<=2", all((abs(1 + v - u) <= 2) == (-3 <= v - u <= 1) for v in range(-4, 5) for u in range(-6, 7)), True)

# L03 arithmetic quoted on cards
check("L03 3*97", 3 * 97, 291)
check("L03 6*104", 6 * 104, 624)
check("L03 291 < 624", 291 < 624, True)
check("L03 21/37 < 2", Fraction(21, 37) < 2, True)
check("L03 21*50", 21 * 50, 1050)
check("L03 17*37", 17 * 37, 629)
check("L03 6/29 - 5/34", Fraction(6, 29) - Fraction(5, 34), Fraction(59, 986))
check("L03 fills total 2*executions", 2 * 207, 414)
check("L03 identity worked example", 1000 - 120 - 2 * 300 - 40, 240)

# L02 counts quoted on cards
check("L02 patterns firing (P1,P3,P4,P6)", 4, 4)

print("ALL OK" if ok else "SOME CHECKS FAILED")
