"""LX1-b round 16: independent re-derivation of every number in L03 and L04 prose, tables and quiz.

Written by the verifier from the printed formulas only (not from the lab twins). Exact arithmetic is Fraction;
the L04 logarithms and standard deviations are Decimal at 60 significant digits, so no float enters.

Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r16/rederive_r16.py <checkout>
"""

import csv
import sys
from decimal import ROUND_HALF_UP, Decimal, getcontext
from fractions import Fraction
from pathlib import Path

getcontext().prec = 60
root = Path(sys.argv[1])


def half_up(q: Fraction, places: int) -> str:
    """Round a non-negative exact value half up to a decimal string with the given places (integer arithmetic)."""
    scaled = q * 10**places
    n = (scaled.numerator * 2 + scaled.denominator) // (2 * scaled.denominator)
    whole, frac = divmod(n, 10**places)
    return f"{whole}.{frac:0{places}d}" if places else str(whole)


def half_up_int(q: Fraction) -> int:
    return (q.numerator * 2 + q.denominator) // (2 * q.denominator)


# ---------------- L03 ----------------
D = 1_000_000
K0 = 4_000_000
delta = Fraction(1, 50)
H = 12
C = K0 + D


def V(m: int, t: int) -> Fraction:
    return Fraction(D) * (1 - delta) ** (-min(t, m))


def K(m: int, t: int) -> Fraction:
    return K0 - (V(m, t) - D)


def L(m: int, t: int) -> Fraction:
    return V(m, t) / K(m, t)


L0 = L(0, 0)


def f(m: int, t: int, phi: Fraction = Fraction(1), beta: Fraction = Fraction(1)) -> Fraction:
    return beta * phi * (L(m, t) - L0)


def depth(m: int, phi: Fraction = Fraction(1), beta: Fraction = Fraction(1)) -> Fraction:
    return max(f(m, t, phi, beta) for t in range(H + 1))


print("L03 baseline L0 = 0.25 exactly:", L0 == Fraction(1, 4), "| L0 printed", half_up(L0, 4))
print("L03 V12 =", float(V(12, 12)), "rounded", half_up_int(V(12, 12)), "| printed 1274345 ; exact 1,274,345.2124 ->",
      half_up(V(12, 12) - D + D, 4))
print("L03 V12 < C:", V(12, 12) < C, "| V12 =", half_up(V(12, 12), 4), "| C =", C)
print("L03 V4(Y) =", half_up(V(4, 4), 4), "rounded int", half_up_int(V(4, 4)))
print("L03 K4(Y) =", half_up(K(4, 4), 4), "rounded int", half_up_int(K(4, 4)))
print("L03 L4(Y) =", half_up(L(4, 4), 4), "exact", float(L(4, 4)))
print("L03 P4 exact", (Fraction(49, 50)) ** 4, float((Fraction(49, 50)) ** 4), "(5764801/6250000)")
print("L03 V4 exact decimal (4 dp):", half_up(V(4, 4), 4), "| 1084165.7847 as printed in M1")
print("L03 K4 exact (4 dp):", half_up(K(4, 4), 4), "| 3915834.2153 in M2")
print("L03 M3 rounding of L4 from V4, K4 rounded:", half_up(Fraction(half_up_int(V(4, 4))) / Fraction(half_up_int(K(4, 4))), 4))
for m, name in ((12, "X"), (4, "Y")):
    print(f"L03 economy {name} depth exact {float(depth(m) * 100):.6f} percent -> {half_up(depth(m) * 100, 2)}")
    print(f"L03 economy {name} first maximising t:", min(t for t in range(H + 1) if f(m, t) == depth(m)))
    print(f"L03 economy {name} E1/E2 depth x100 4dp:", half_up(depth(m) * 100, 6))
dx, dy = depth(12), depth(4)
print("L03 X deeper:", dx > dy, "| difference exact x100 =", float((dx - dy) * 100), "->", half_up(100 * (dx - dy), 2))
print("L03 printed-difference check 9.20-2.69 =", Fraction("9.20") - Fraction("2.69"))
print("L03 Part D ratio exact:", float(depth(12) / depth(4)), "->", half_up(depth(12) / depth(4), 4))
for phi, beta in ((Fraction(1, 2), Fraction(1)), (Fraction(1), Fraction(1)), (Fraction(3), Fraction(1))):
    r = depth(12, phi, beta) / depth(4, phi, beta)
    print(f"L03 Part D phi={phi} beta={beta} ratio {half_up(r, 4)}")
print("L03 square variant ratio:", float((depth(12) / depth(4)) ** 2))
# depth by m and monotonicity
ds = [depth(m) for m in range(H + 1)]
print("L03 depth m table (percent 2dp):", [half_up(100 * d, 2) for d in ds])
print("L03 never falls:", all(ds[m] <= ds[m + 1] for m in range(H)), "| strict steps:", all(ds[m] < ds[m + 1] for m in range(H)))
print("L03 Cor 3.3 strict for all m'<m pairs:", all(ds[a] < ds[b] for a in range(H + 1) for b in range(a + 1, H + 1)))
print("L03 Cor 3.4 ratio independent of phi,beta:",
      len({depth(12, p, b) / depth(4, p, b) for p in (Fraction(1, 2), Fraction(1), Fraction(3), Fraction(7, 3))
           for b in (Fraction(1), Fraction(5, 2))}) == 1)
# Prop 3.2(b) closed form at m=12, 4
for m in (12, 4):
    Vm = V(m, m)
    closed = Vm / (K0 + D - Vm) - Fraction(D) / K0
    print(f"L03 Prop3.2(b) closed form m={m}: {float(closed):.10f} vs depth {float(depth(m)):.10f} equal={closed == depth(m)}")
# Prop 3.2(a) numerical
print("L03 V_t <= V_m for all t, m=0..12:", all(V(m, t) <= V(m, m) for m in range(H + 1) for t in range(H + 1)))
print("L03 V_m < C for all m:", all(V(m, m) < C for m in range(H + 1)))
print("L03 K_t > 0 all:", all(K(m, t) > 0 for m in range(H + 1) for t in range(H + 1)))
# Remark 4.2 / R1: K_t = C - V_t
print("L03 K_t == C - V_t identity:", all(K(m, t) == C - V(m, t) for m in range(H + 1) for t in range(H + 1)))
# Problem P2 at m=0
print("L03 P2 depth(0)=0:", depth(0) == 0)
# Problem E3 count of unchanged index for Y
idx_y = [Fraction(49, 50) ** min(t, 4) for t in range(H + 1)]
print("L03 E3 unchanged periods Y:", sum(1 for t in range(1, H + 1) if idx_y[t] == idx_y[t - 1]))
# Quiz Q3: exact depth Y
print("L03 Quiz Q3 exact depth Y percent:", float(depth(4) * 100))
print("L03 Quiz Q8: V12 exact", float(V(12, 12)))
# Lemma 3.1 identity check at random rational points
import random  # noqa: E402

rng = random.Random(16)
ok = True
for _ in range(200):
    x = Fraction(D) + Fraction(rng.randint(0, 10**6), 10**6) * (C - D)
    y = Fraction(D) + Fraction(rng.randint(0, 10**6), 10**6) * (C - D)
    if x >= y:
        continue
    lam = lambda z: z / (C - z)  # noqa: E731
    ok &= lam(y) - lam(x) == Fraction(C) * (y - x) / ((C - x) * (C - y)) and lam(y) > lam(x)
print("L03 Lemma 3.1 identity and monotone at 200 random points:", ok)

# ---------------- L04 ----------------
csv_path = root / "course/assets/data/market/fx_monthly.csv"
with csv_path.open(encoding="utf-8", newline="") as h:
    reader = csv.DictReader(h)
    fields = reader.fieldnames
    rows = list(reader)
print("L04 csv header:", fields)
months = [r["month"] for r in rows]
print("L04 rows:", len(rows), "first", months[0], "last", months[-1])
gbp = [r["GBP"] for r in rows]
print("L04 GBP blanks:", sum(1 for g in gbp if g.strip() == ""))
print("L04 GBP non-decimal cells:", [g for g in gbp if not all(ch in "0123456789." for ch in g)][:5])


def ym(s: str) -> int:
    y, mm = s.split("-")
    return int(y) * 12 + int(mm) - 1


print("L04 contiguous months:", all(ym(months[i + 1]) == ym(months[i]) + 1 for i in range(len(months) - 1)))
rates = [Fraction(g) for g in gbp]
print("L04 all rates positive:", all(r > 0 for r in rates))
changes = [(months[i], rates[i] / rates[i - 1], rates[i] == rates[i - 1]) for i in range(1, len(rates))]
zeros = [m for m, _, z in changes if z]
print("L04 exactly zero months:", len(zeros), zeros)
print("L04 nonzero changes:", len(changes) - len(zeros))


def dec_ln(q: Fraction) -> Decimal:
    return (Decimal(q.numerator) / Decimal(q.denominator)).ln()


logs = [(m, dec_ln(ratio)) for m, ratio, _ in changes]
w1 = logs
w2 = [(m, v) for m, v in logs if m >= "2000-01"]
print("L04 window one changes:", len(w1), "| window two changes:", len(w2), "| first window-two change", w2[0][0],
      "| its base month", months[months.index("2000-01") - 1])


def sd(vals: list[Decimal]) -> Decimal:
    n = len(vals)
    mean = sum(vals) / n
    return (sum((v - mean) ** 2 for v in vals) / (n - 1)).sqrt()


def dround(d: Decimal, places: int) -> str:
    return str(d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


s1 = sd([v for _, v in w1])
s2 = sd([v for _, v in w2])
print("L04 sd window one:", s1, "->", dround(s1, 6), "| 0.027935 printed")
print("L04 sd window two:", s2, "->", dround(s2, 6), "| 0.024700 printed")
print("L04 difference s2-s1:", s2 - s1, "->", dround(s2 - s1, 6), "| printed -0.003236")
print("L04 printed-figures difference:", Decimal("0.024700") - Decimal("0.027935"))
print("L04 ratio s2/s1:", s2 / s1, "->", dround(s2 / s1, 4), "| printed 0.8842")
big1 = max(w1, key=lambda it: abs(it[1]))
big2 = max(w2, key=lambda it: abs(it[1]))
print("L04 largest window one:", big1[0], dround(big1[1], 6), "| abs", dround(abs(big1[1]), 6), "| printed 1985-03 0.135846")
print("L04 largest window two:", big2[0], dround(big2[1], 6), "| abs", dround(abs(big2[1]), 6), "| printed 2008-10 -0.096575")
print("L04 ties in abs window one:", sum(1 for _, v in w1 if abs(v) == abs(big1[1])))
print("L04 ties in abs window two:", sum(1 for _, v in w2 if abs(v) == abs(big2[1])))
# identity sum of changes = ln(last/base)
for name, w, base in (("one", w1, rates[0]), ("two", w2, rates[months.index("1999-12")])):
    tot = sum(v for _, v in w)
    target = (rates[-1] / base)
    print(f"L04 identity window {name}: |sum - ln(last/base)| =", float(abs(tot - dec_ln(target))), "<= 1e-12:",
          abs(tot - dec_ln(target)) <= Decimal("1e-12"))
# E2: simple change for 2008-10
v2008 = dict(w2)["2008-10"]
simple = (v2008.exp() - 1)
print("L04 E2 simple change 2008-10:", simple, "->", dround(simple, 6), "| page says -0.092058")
# R2: h = tanh(z/2) for z = 0.135846...(unrounded largest window one)
z = abs(big1[1])
e = z.exp()
h_exact = (e - 1) / (e + 1)
print("L04 R2 h exact:", h_exact, "->", dround(h_exact, 6), "| four dp", dround(h_exact, 4))
bound_h = Decimal("0.0678")
bound = ((1 + bound_h) / (1 - bound_h)).ln()
print("L04 R2 bound at h=0.0678:", dround(bound, 6), "| quiz 0.135808 ->", dround(bound, 4), "| below z:", bound < z)
# M1
r11 = Decimal("1.3750") / Decimal("1.2500")
print("L04 M1 ratio", r11, "ln", dround(r11.ln(), 10), "->", dround(r11.ln(), 6), "diff", dround(Decimal("0.1") - r11.ln(), 7))
print("L04 M1 ln(1.1)", dround(Decimal("1.1").ln(), 6))
# M2
vals = [Decimal("0.01"), Decimal("0.03"), Decimal("-0.02")]
print("L04 M2 mean", dround(sum(vals) / 3, 6), "| disp", dround(sd(vals), 6), "| exact 19/15000 check",
      sum((v - sum(vals) / 3) ** 2 for v in vals) == Decimal(19) / Decimal(15000))
# M3 count
count = sum(1 for m in months if "2000-01" <= m <= "2026-09")
print("L04 M3 months 2000-01..2026-09:", count, "| first change uses", months[months.index("2000-01") - 1])
# Part A model
print("L04 Part A model changes 11 -> zero dispersion, n=11:", 12 - 1)
# P2 bound check on window one at the largest move
print("L04 misconception 3: ln 1.1 - 0.1 =", dround(Decimal("0.1") - Decimal("1.1").ln(), 6))
