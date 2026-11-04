# Independent re-implementation of the L04 outcomes numbers (not an import of the lab).
# Draws use randrange(13)-6 and randrange(9)-4, which give the same uniform integers as randint.
import random
from decimal import Decimal, ROUND_HALF_UP, getcontext
from fractions import Fraction

getcontext().prec = 60
rng = random.Random(20261103)
H = 24
rows = []
for t in range(1, H + 1):
    U = rng.randrange(13) - 6        # realised draw, -6..6
    V = rng.randrange(9) - 4         # forecast draw, -4..4
    y = 100 + U
    f = 101 + V
    rows.append((t, f, y, f - y))

def hit(e, band=2):
    return abs(e) <= band

def half_away_4(x):
    d = Decimal(x.numerator) / Decimal(x.denominator)
    q = d.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)  # ROUND_HALF_UP is away from zero on ties
    return str(q)

def floor_rule(x):
    s = abs(x) * 10000 + Fraction(1, 2)
    n = s.numerator // s.denominator
    return ("-" if x < 0 else "") + f"{n // 10000}.{n % 10000:04d}"

errs = [r[3] for r in rows]
hits = sum(hit(e) for e in errs)
hr = Fraction(hits, H)
bias = Fraction(sum(errs), H)
print("hits", hits, "of", H, "hit rate", hr, half_away_4(hr), floor_rule(hr))
print("bias", bias, half_away_4(bias), floor_rule(bias), "sum", sum(errs))
mae = Fraction(sum(abs(e) for e in errs), H)
print("MAE", mae, float(mae))
for label, sub in (("first12", rows[:12]), ("last12", rows[12:])):
    e = [r[3] for r in sub]
    h = Fraction(sum(hit(x) for x in e), 12)
    b = Fraction(sum(e), 12)
    print(label, "hr", h, half_away_4(h), "bias", b, half_away_4(b), floor_rule(b))
for r in rows:
    print(r)
# Part C hand-built
ce = [3, -3, 3, -3]
print("partC hit rate", Fraction(sum(hit(e) for e in ce), 4), "bias", Fraction(sum(ce), 4), "MAE", Fraction(sum(abs(e) for e in ce), 4))
# Part D exact enumeration: P(hit) and E[e] under A1
pairs = [(1 + v - u) for v in range(-4, 5) for u in range(-6, 7)]
print("pairs", len(pairs), "P(hit)", Fraction(sum(hit(e) for e in pairs), len(pairs)), "E[e]", Fraction(sum(pairs), len(pairs)))
# Own check of the hit probability by a different route: count per V
cnt = 0
for v in range(-4, 5):
    cnt += sum(1 for u in range(-6, 7) if abs((101 + v) - (100 + u)) <= 2)
print("hit count by V route", cnt, Fraction(cnt, 117))
# Rounding check on 11/3, 19/6, -7/3, 44/117, 20/39
for x in [Fraction(11, 3), Fraction(19, 6), Fraction(-7, 3), Fraction(44, 117), Fraction(20, 39), Fraction(41, 12)]:
    print("round", x, floor_rule(x), half_away_4(x))
