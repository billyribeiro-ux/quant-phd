"""Independent recomputation of every number on the L03 and L04 pages (verifier round 5).

Does not import either lab twin. L03 uses exact fractions.Fraction arithmetic. L04 reads the embedded CSV
with the csv module and computes logs with decimal.Decimal at 60 significant digits, so the unrounded values
are not limited by float precision. Rounding is half up, applied once, to the printed places.
Run with: python3 -I recompute_r5.py <checkout>
"""

from __future__ import annotations

import csv
import math
import sys
from decimal import ROUND_HALF_UP, Context, Decimal
from fractions import Fraction
from pathlib import Path

root = Path(sys.argv[1])

# ---------------------------------------------------------------- L03 (exact)
D = Fraction(1_000_000)
N0 = Fraction(4_000_000)
DELTA = Fraction(1, 50)
H = 12
PHI = Fraction(1)
BETA = Fraction(1)
C = N0 + D


def P(m: int, t: int) -> Fraction:
    return (1 - DELTA) ** min(t, m)


def V(m: int, t: int) -> Fraction:
    return D / P(m, t)


def L(m: int, t: int) -> Fraction:
    return V(m, t) / (N0 - (V(m, t) - D))


def f(m: int, t: int) -> Fraction:
    return BETA * PHI * (L(m, t) - L(0, 0))


def depth(m: int) -> Fraction:
    return max(f(m, t) for t in range(H + 1))


def first_t(m: int) -> int:
    top = depth(m)
    return next(t for t in range(H + 1) if f(m, t) == top)


def half_up(x: Fraction, places: int) -> str:
    scaled = x * 10**places
    n = math.floor(scaled + Fraction(1, 2))
    whole, frac = divmod(n, 10**places)
    return f"{whole}.{frac:0{places}d}"


print("L03 depth X (m=12) percent:", half_up(100 * depth(12), 2), "exact float", float(100 * depth(12)))
print("L03 depth Y (m=4) percent:", half_up(100 * depth(4), 2), "exact float", float(100 * depth(4)))
print("L03 first t X:", first_t(12), " first t Y:", first_t(4))
diff = 100 * (depth(12) - depth(4))
print("L03 difference X-Y exact:", float(diff), "rounded:", half_up(diff, 2))
print("L03 printed-difference of rounded depths: 9.20 - 2.69 =", Decimal("9.20") - Decimal("2.69"))
print("L03 exact depth(12) - depth(4) lower/upper bound check: X > Y", depth(12) > depth(4))
never_falls = all(depth(m) <= depth(m + 1) for m in range(H))
strict = all(depth(m) < depth(m + 1) for m in range(H))
print("L03 never falls:", never_falls, " strict every step m=0..11:", strict)
print("L03 depth(0) =", depth(0), " depth values (percent, 2dp):", [half_up(100 * depth(m), 2) for m in range(H + 1)])
for phi, beta in ((Fraction(1, 2), Fraction(1)), (Fraction(1), Fraction(1)), (Fraction(3), Fraction(1))):
    # depth scales with phi*beta: recompute with the parameters explicitly
    def fp(m: int, t: int) -> Fraction:
        return beta * phi * (L(m, t) - L(0, 0))

    dx = max(fp(12, t) for t in range(H + 1))
    dy = max(fp(4, t) for t in range(H + 1))
    print("L03 ratio X/Y phi*beta =", phi * beta, "exact", float(dx / dy), "2dp4:", half_up(dx / dy, 4))
r = depth(12) / depth(4)
print("L03 squared-premium ratio r^2 =", float(r * r), " r =", float(r), " r^2 != r:", r * r != r)
print("L03 V_12 cents exact:", float(V(12, 12)), "rounded:", half_up(V(12, 12), 0))
print("L03 V_4 cents exact:", float(V(4, 4)), "rounded:", half_up(V(4, 4), 0))
N4 = N0 - (V(4, 4) - D)
print("L03 M1 P_4 exact:", P(4, 4), float(P(4, 4)))
print("L03 M2 N_4 exact:", float(N4), "rounded:", half_up(N4, 0))
print("L03 M3 L_4 exact:", float(V(4, 4) / N4), "4dp:", half_up(V(4, 4) / N4, 4))
print("L03 closed-form check depth(12) = V_m formula:",
      depth(12) == BETA * PHI * (Fraction(V(12, 12)) / (C - V(12, 12)) - D / N0))
print("L03 V_m < C (Assumption 1.2):", V(12, 12) < C, " V_m < C for m=4:", V(4, 4) < C)
print("L03 remark 4.2 V_12 < N0 + D cents:", float(V(12, 12)), "<", float(C))
print("L03 Part A baseline leverage:", half_up(L(0, 0), 4))

# ---------------------------------------------------------------- L04 (Decimal, 60 digits)
ctx = Context(prec=60, rounding=ROUND_HALF_UP)
rows: list[tuple[str, str]] = []
with (root / "course/assets/data/market/fx_monthly.csv").open(encoding="utf-8", newline="") as handle:
    reader = csv.DictReader(handle)
    print("L04 CSV header:", reader.fieldnames)
    for rec in reader:
        rows.append((rec["month"], rec["GBP"]))
blank = [m for m, v in rows if v.strip() == ""]
nondec = [m for m, v in rows if v.strip() != "" and not all(ch.isdigit() or ch == "." for ch in v)]
print("L04 rows:", len(rows), rows[0][0], rows[-1][0], " blanks:", len(blank), " non-decimal:", len(nondec))
gbp = [(m, Decimal(v)) for m, v in rows]
changes = []
for (m0, x0), (m1, x1) in zip(gbp, gbp[1:]):
    changes.append((m1, ctx.ln(ctx.divide(x1, x0))))
zero_months = [m1 for (m0, x0), (m1, x1) in zip(gbp, gbp[1:]) if x1 == x0]
print("L04 zero-change months:", zero_months, "count", len(zero_months), "nonzero", len(changes) - len(zero_months))
w1 = changes
w2 = [c for c in changes if c[0] >= "2000-01"]
print("L04 window one n:", len(w1), w1[0][0], w1[-1][0], " window two n:", len(w2), w2[0][0], w2[-1][0])


def sd(vals: list[Decimal]) -> Decimal:
    n = len(vals)
    mean = ctx.divide(sum(vals, Decimal(0)), Decimal(n))
    ss = sum(((v - mean) ** 2 for v in vals), Decimal(0))
    return ctx.sqrt(ctx.divide(ss, Decimal(n - 1)))


s1 = sd([c for _, c in w1])
s2 = sd([c for _, c in w2])
print("L04 sd window one:", s1, "-> 6dp", s1.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))
print("L04 sd window two:", s2, "-> 6dp", s2.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))
print("L04 difference two-one unrounded:", s2 - s1, "-> 6dp", (s2 - s1).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))
print("L04 printed-subtraction 0.024700 - 0.027935 =", Decimal("0.024700") - Decimal("0.027935"))
print("L04 ratio two/one unrounded:", ctx.divide(s2, s1), "-> 4dp", ctx.divide(s2, s1).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
big1 = max(w1, key=lambda c: abs(c[1]))
big2 = max(w2, key=lambda c: abs(c[1]))
print("L04 largest window one:", big1[0], big1[1], " largest window two:", big2[0], big2[1])
print("L04 largest window one 6dp:", abs(big1[1]).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP),
      " window two signed 6dp:", big2[1].quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))
# E2: simple change for 2008-10 from unrounded log change
simple = ctx.exp(big2[1]) - 1
print("L04 E2 simple change 2008-10 unrounded:", simple, "-> 6dp", simple.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))
# identity
for name, win, start_month in (("one", w1, gbp[0][0]), ("two", w2, "1999-12")):
    start_rate = dict(gbp)[start_month]
    last = gbp[-1][1]
    total = sum((c for _, c in win), Decimal(0))
    print("L04 identity window", name, "sum minus ln(last/start):", total - ctx.ln(ctx.divide(last, start_rate)))
# window two start rate check and 2000-01 index
print("L04 rate 1999-12:", dict(gbp)["1999-12"], " rate 2000-01:", dict(gbp)["2000-01"])

# R2 and P2 bound numbers
L_big = abs(big1[1])
h_exact = ctx.tanh(L_big / 2) if hasattr(ctx, "tanh") else None
# tanh via exp
ex = ctx.exp(L_big)
h_exact = (ex - 1) / (ex + 1)
print("L04 R2 h exact (tanh(L/2)) unrounded:", h_exact, "-> 6dp", h_exact.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP))
bound = ctx.ln(ctx.divide(Decimal("1.0678"), Decimal("0.9322")))
print("L04 Q bound at h=0.0678: ln(1.0678/0.9322) =", bound, "-> 6dp", bound.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP),
      "-> 4dp", bound.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP))
print("L04 R2 claim: 0.0678 < exact h:", Decimal("0.0678") < h_exact)
print("L04 bound at 0.0678 less than largest move:", bound < L_big)
# misconception 3 and M1
ln11 = ctx.ln(Decimal("1.1"))
print("L04 ln 1.1 =", ln11, "-> 6dp", ln11.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP),
      " 0.1 - ln1.1 =", Decimal("0.1") - ln11)
# M2
vals = [Decimal("0.01"), Decimal("0.03"), Decimal("-0.02")]
mean = sum(vals) / 3
ss = sum((v - mean) ** 2 for v in vals)
print("L04 M2 mean:", mean, " sum sq dev:", ss, " 19/15000 =", Decimal(19) / Decimal(15000), " sd:", ctx.sqrt(ss / 2))
# M3
months_2000_2026 = (2026 - 2000) * 12 + (9 - 1) + 1
print("L04 M3 months 2000-01..2026-09:", months_2000_2026)
# Part A model: 12 rates -> 11 changes, all exactly zero
print("L04 part A changes:", 12 - 1)
