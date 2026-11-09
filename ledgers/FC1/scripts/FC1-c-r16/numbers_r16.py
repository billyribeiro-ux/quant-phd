"""Round 16, FC1-c: re-derive the page's fixture, lab-1 and rounding numbers with exact Fractions (no reference module)."""
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_EVEN

def rnd_half_away(x: F) -> int:
    # nearest integer, a half going away from zero
    s = 1 if x >= 0 else -1
    a = abs(x)
    n = int(a)
    frac = a - n
    return s * (n + (1 if frac >= F(1, 2) else 0))

def coupon_cents(face: int, bps: int) -> int:
    return rnd_half_away(F(face) * bps / 10000)

def events(face: int, bps: int, periods: int) -> list[tuple[int, int]]:
    c = coupon_cents(face, bps)
    out = []
    for t in range(1, periods + 1):
        amt = c + (face if t == periods else 0)
        out.append((t, amt))
    return out

def pv_exact(evs, bps: int) -> F:
    y = F(bps, 10000)
    return sum((F(a) / (1 + y) ** t for t, a in evs), F(0))

def price(evs, bps: int) -> int:
    return rnd_half_away(pv_exact(evs, bps))

# Fixture A
evA = events(10000, 500, 1); print("A events", evA, "price@500", price(evA, 500), "exact", pv_exact(evA, 500))
# Fixture B
evB = evA; print("B exact at -500", pv_exact(evB, -500), float(pv_exact(evB, -500)), price(evB, -500))
# Fixture C
print("C events", events(10001, 5000, 2), "coupon exact", F(10001) * 5000 / 10000)
# Fixture D
print("D events", events(1, 5000, 1), "coupon exact", F(1) * 5000 / 10000)
# Fixture F
evF = events(1, 0, 1); print("F events", evF, "exact", pv_exact(evF, 10000), "half-away", price(evF, 10000), "half-even", round(pv_exact(evF, 10000)))
# Fixture G
evG = events(10001, 0, 1); print("G events", evG, "exact", pv_exact(evG, 10000), "price", price(evG, 10000))
# Rounding fixture
evR = events(10000, 500, 3); print("R events", evR, "exact", float(pv_exact(evR, 400)), "price", price(evR, 400))
terms = [rnd_half_away(F(a) / (1 + F(400, 10000)) ** t) for t, a in evR]
print("R term-by-term", terms, sum(terms))
# Lab 1 bond: face 100000, 500 bps, 3 periods, 400 bps
evL1 = events(100000, 500, 3); ex = pv_exact(evL1, 400)
print("L1 events", evL1, "exact", float(ex), "exact 6dp", f"{float(ex):.6f}", "price", price(evL1, 400))
# Fixture E
print("E trade", -(10 * 9850), "seller", 10 * 9850)
# new tests
print("NEW coupon 20001 bps events", events(10000, 20001, 1))
print("NEW trade price 1e9", -(10 * 10**9))
print("bond 15000 bps events", events(10000, 15000, 1))
