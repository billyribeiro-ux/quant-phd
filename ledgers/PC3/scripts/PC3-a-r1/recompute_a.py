"""Independent recomputation of every number in the PC3 slice a (hub, L01-L03), written by the round-1 verifier.

Standard library only. Does not import any course code. Prints every value the pages state, to the
precision the page states it, so each row can be compared by eye and by the verifier's ledger.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction
from decimal import Decimal, getcontext

getcontext().prec = 40


def hdr(title: str) -> None:
    print(f"== {title}")


# ---------------- Hub ----------------
hdr("hub placement")
print("die expectation", Fraction(sum(range(1, 7)), 6), float(Fraction(sum(range(1, 7)), 6)))
print("PV 100/1.1", float(Decimal(100) / Decimal("1.1")))
print("mastery 8 of 10 =", Fraction(8, 10), " 7 of 10 =", Fraction(7, 10))
print("hours lessons share", Fraction(36, 50), " project share", Fraction(14, 50))
print("project split sum 2+6+4+2 =", 2 + 6 + 4 + 2)

# ---------------- L01 ----------------
hdr("L01 product bounds")
lo = Fraction(20) * 2 * 300
hi = Fraction(60) * 10 * 390
print("lower", lo, "upper", hi, "ratio", hi / lo, float(hi / lo))
w = math.log(float(hi / lo))
print("ln19.5", f"{w:.10f}")
print("geo mean", f"{math.sqrt(float(lo * hi)):.10f}", "decimal", Decimal(int(lo * hi)).sqrt())
f1, f2, f3 = math.log(3), math.log(5), math.log(1.3)
print("factor widths", f"{f1:.10f} {f2:.10f} {f3:.10f}", "sum", f"{f1 + f2 + f3:.10f}")

hdr("L01 narrowing shares")
base = w
r_sym = base - math.log(13)  # total with symbols [20,40]: ln2 + ln5 + ln1.3 = ln13
r_qu = base - math.log(7.8)  # quote updates [4,8]: ln3 + ln2 + ln1.3 = ln 7.8
r_min = base - math.log(15 * 360 / 330)  # minutes [330,360]
print("reduction symbols", f"{r_sym:.10f}", "total", f"{math.log(13):.10f}")
print("reduction quotes", f"{r_qu:.10f}", "share", f"{r_qu / base * 100:.4f}%", "total", f"{math.log(7.8):.10f}")
print("reduction minutes", f"{r_min:.10f}", "share", f"{r_min / base * 100:.4f}%", "total", f"{math.log(15*360/330):.10f}")
print("E2 shares of 2.9704:", f"{0.9163 / 2.9704:.6f}", f"{0.1754 / 2.9704:.6f}")
print("R1: half total", f"{base / 2:.4f}", "ln5", f"{math.log(5):.4f}", "ln3", f"{math.log(3):.4f}")
print("R3: ln(3/2)", f"{math.log(1.5):.4f}", "ln(2.5/1.01)", f"{math.log(2.5 / 1.01):.4f}", "ln 2.5", f"{math.log(2.5):.4f}")
print("E3: ln16.5", f"{math.log(16.5):.4f}", "diff", f"{math.log(19.5) - math.log(16.5):.6f}")

hdr("L01 Taylor bounds")
for n, x in [(10, Fraction(1, 100)), (10, Fraction(1, 20)), (5, Fraction(1, 100)), (5, Fraction(1, 20)),
             (2, Fraction(1, 100)), (2, Fraction(1, 20))]:
    rem = (1 + x) ** n - 1 - n * x
    bnd = Fraction(n * (n - 1), 2) * (1 + x) ** (n - 2) * x * x
    print(f"n={n} x={x}: rem={float(rem):.10f} bound={float(bnd):.10f} rem/bound={float(rem / bnd):.6f}"
          f" bound/rem-1={float(bnd / rem - 1):.6f}")
print("E1 ratio decimal", Decimal("0.0046221254") / Decimal("0.0048728552"))
print("Ex1.7 bound/rem - 1 exact (0.0048728552/0.0046221254)-1 =",
      Decimal("0.0048728552") / Decimal("0.0046221254") - 1)
print("M3 exact remainder", Fraction(1331, 1000) - 1 - Fraction(3, 10), " bound", 3 * Fraction(11, 10) * Fraction(1, 100))
print("ln4", f"{math.log(4):.7f}", "ln16", f"{math.log(16):.4f}")
print("geo mean 4dp", f"{math.sqrt(2808000000):.4f}")

# ---------------- L02 ----------------
hdr("L02 enumerations")
flips2 = list(itertools.product("HT", repeat=2))
p_at_least_one = Fraction(sum(1 for o in flips2 if "H" in o), 4)
p_both = Fraction(1, 4)
print("P(both|>=1H)", p_both / p_at_least_one, " P(both|first H)", p_both / Fraction(1, 2),
      " P(>=1H|both)", Fraction(1))
# urn
balls = ["r1", "r2", "r3", "b1", "b2"]
pairs = [(a, b) for a in balls for b in balls if a != b]
red = {"r1", "r2", "r3"}
print("urn pairs", len(pairs), "P(second red)", Fraction(sum(b in red for _, b in pairs), 20),
      "P(both red)", Fraction(sum(a in red and b in red for a, b in pairs), 20),
      "P(second red|first blue)", Fraction(sum(b in red for a, b in pairs if a.startswith("b")),
                                           sum(1 for a, _ in pairs if a.startswith("b"))))
# Monty Hall, both rules, by exact enumeration with independent code
def monty(rule: str) -> tuple[Fraction, Fraction]:
    stay = switch = total = Fraction(0)
    for car, pick in itertools.product(range(3), range(3)):
        for opened in range(3):
            if opened in (pick,):
                continue
            goats = [d for d in range(3) if d != pick and d != car]
            if rule == "A":
                if opened not in goats:
                    continue
                pr = Fraction(1, len(goats))
            else:
                if opened == car:
                    continue
                pr = Fraction(1, 2)
            wt = Fraction(1, 9) * pr
            total += wt
            if pick == car:
                stay += wt
            other = [d for d in range(3) if d not in (pick, opened)][0]
            if other == car:
                switch += wt
    return stay / total, switch / total


print("Monty rule A (stay, switch)", monty("A"))
print("Monty rule B (stay, switch)", monty("B"))
# bag
print("bag P(red)", Fraction(1, 2) * Fraction(3, 4) + Fraction(1, 2) * Fraction(1, 4),
      "P(bag1|red)", (Fraction(1, 2) * Fraction(3, 4)) / (Fraction(1, 2) * Fraction(3, 4) + Fraction(1, 2) * Fraction(1, 4)))
# M1, M2, M3, P3-type checks
print("L02 M1 P(sum7|first3)", Fraction(1, 36) / Fraction(6, 36))
print("L02 M2 P(B)", Fraction(1, 2) * Fraction(3, 10) + Fraction(1, 5) * Fraction(7, 10),
      "P(A|B)", (Fraction(1, 2) * Fraction(3, 10)) / (Fraction(29, 100)))
print("L02 M3 both red", Fraction(4, 6) * Fraction(3, 5))
print("L02 E1 57/64", 1 - Fraction(1, 64) - Fraction(6, 64))
print("L02 quiz 0.333333 vs 1/3", float(Fraction(1, 3)))

# ---------------- L03 ----------------
hdr("L03 games")
FAIR = ((100, Fraction(1, 2)), (-100, Fraction(1, 2)))
BIAS = ((150, Fraction(1, 2)), (-100, Fraction(1, 2)))
RULES = {
    "play all": lambda h: False,
    "first win": lambda h: bool(h) and h[-1] > 0,
    "first loss": lambda h: bool(h) and h[-1] < 0,
    "total>=100": lambda h: sum(h) >= 100,
    "|total|>=200": lambda h: sum(h) >= 200 or sum(h) <= -200,
}


def expect(game, rule, horizon=6):
    total = Fraction(0)
    for seq in itertools.product(game, repeat=horizon):
        wt = Fraction(1)
        hist: tuple[int, ...] = ()
        for x, p in seq:
            wt *= p
        stopped = False
        for x, _ in seq:
            hist = (*hist, x)
            if rule(hist):
                stopped = True
                break
        total += wt * sum(hist)
    return total


for name, rule in RULES.items():
    print("fair", name, expect(FAIR, rule), " biased", expect(BIAS, rule), float(expect(BIAS, rule)))

hdr("L03 reroll and R1")
cont = Fraction(sum(100 * g for g in range(1, 7)), 6) - 100
vals = []
for f in range(1, 7):
    vals.append(max(Fraction(100 * f), cont))
print("continuation", cont, "value", sum(vals) / 6, float(sum(vals) / 6), "gain", sum(vals) / 6 - 350)
best = max(sum((Fraction(100 * f) if bits[f - 1] else cont) for f in range(1, 7)) / 6
           for bits in itertools.product((0, 1), repeat=6))
print("best of 64 policies", best)
# R1: two-turn fair game, rule stops at the turn with larger cumulative total
paths = [(100, 100), (100, -100), (-100, 100), (-100, -100)]
tot = []
for a, b in paths:
    w1, w2 = a, a + b
    tot.append(w1 if w1 > w2 else w2)
print("R1 totals", tot, "expected", Fraction(sum(tot), 4))
print("E2 hub: 625/8-150 =", Fraction(625, 8) - 150, float(Fraction(625, 8) - 150))
print("E3: 1150/3-350 =", Fraction(1150, 3) - 350, float(Fraction(1150, 3) - 350))
print("M2 p", Fraction(1, 3))
print("M3 two-stage", Fraction(1, 2) * 100 + Fraction(1, 2) * (-50 + 100 * Fraction(7, 2)))
print("P3 threshold: 100f<250 for f in 1..6:", [f for f in range(1, 7) if 100 * f < 250])
